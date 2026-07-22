import os
from pathlib import Path
import re
import shutil
import subprocess

import django
from django.test import SimpleTestCase


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


class EnvironmentContainmentTests(SimpleTestCase):
    def test_real_environment_files_are_ignored_and_examples_are_trackable(self):
        ignored_names = (".env", ".env.prod", ".env.local", ".env.staging")
        for ignored_name in ignored_names:
            with self.subTest(ignored_name=ignored_name):
                result = subprocess.run(
                    ["git", "check-ignore", "--no-index", "--quiet", "--", ignored_name],
                    cwd=REPOSITORY_ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0)

        for example_name in (".env.example", ".env.prod.example"):
            with self.subTest(example_name=example_name):
                result = subprocess.run(
                    ["git", "check-ignore", "--no-index", "--quiet", "--", example_name],
                    cwd=REPOSITORY_ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 1)

    def test_safe_production_example_contains_names_not_secret_payloads(self):
        example = (REPOSITORY_ROOT / ".env.prod.example").read_text(encoding="utf-8")
        self.assertNotRegex(example, r"(?m)^(SECRET_KEY|OPENAI_API_KEY|PAGESPEED_API_KEY)=")
        for secret_name in (
            "SECRET_KEY_SECRET_NAME",
            "OPENAI_API_KEY_SECRET_NAME",
            "PAGESPEED_API_KEY_SECRET_NAME",
        ):
            self.assertRegex(example, rf"(?m)^{secret_name}=")
        self.assertIn("ENABLE_REMOTE_URL_TOOLS=false", example)

    def test_dockerfile_uses_narrow_copies_and_context_excludes_secrets(self):
        dockerfile = (REPOSITORY_ROOT / "Dockerfile").read_text(encoding="utf-8")
        copy_lines = [line.strip() for line in dockerfile.splitlines() if line.strip().upper().startswith("COPY ")]

        self.assertFalse(any(re.match(r"^COPY\s+\.\s+", line, re.IGNORECASE) for line in copy_lines))
        self.assertFalse(any(".env" in line.lower() for line in copy_lines))
        self.assertEqual(
            copy_lines,
            [
                "COPY requirements.txt /app/requirements.txt",
                "COPY manage.py /app/manage.py",
                "COPY pi_development /app/pi_development",
                "COPY static /app/static",
            ],
        )

        dockerignore = (REPOSITORY_ROOT / ".dockerignore").read_text(encoding="utf-8").splitlines()
        for required_pattern in (".env", ".env.*", ".git/", ".venv/", "*.sqlite3", "credentials/", "*.pem", "*.key"):
            self.assertIn(required_pattern, dockerignore)

    def test_cloud_build_context_excludes_local_and_generated_state(self):
        gcloudignore = (REPOSITORY_ROOT / ".gcloudignore").read_text(encoding="utf-8").splitlines()
        for required_pattern in (
            ".env",
            ".env.*",
            ".git",
            ".venv/",
            "venv/",
            "*.sqlite3",
            "*.db",
            "*.log",
            "__pycache__/",
            "staticfiles/",
            "credentials/",
        ):
            self.assertIn(required_pattern, gcloudignore)


class DeploymentPreflightTests(SimpleTestCase):
    @staticmethod
    def _find_bash():
        discovered = shutil.which("bash")
        if discovered:
            return Path(discovered)
        for candidate in (
            Path(r"C:\Program Files\Git\bin\bash.exe"),
            Path(r"C:\Program Files (x86)\Git\bin\bash.exe"),
        ):
            if candidate.exists():
                return candidate
        return None

    def _preflight_environment(self):
        environment = {
            name: os.environ[name]
            for name in ("PATH", "SYSTEMROOT", "WINDIR", "TEMP", "TMP")
            if name in os.environ
        }
        environment.update(
            {
                "SITE_URL": "https://example.com",
                "ALLOWED_HOSTS": "example.com",
                "CSRF_TRUSTED_ORIGINS": "https://example.com",
            }
        )
        return environment

    def _run_preflight(self, environment):
        bash = self._find_bash()
        if not bash:
            self.skipTest("A Bash runtime is required to execute deploy.sh preflight tests.")
        return subprocess.run(
            [str(bash), "deploy.sh", "--validate-only"],
            cwd=REPOSITORY_ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_missing_secret_name_stops_before_cloud_build(self):
        result = self._run_preflight(self._preflight_environment())
        output = f"{result.stdout}\n{result.stderr}"
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("SECRET_KEY_SECRET_NAME", output)
        self.assertNotIn("Construyendo imagen", output)

    def test_plain_secret_variable_is_rejected_without_reading_its_value(self):
        for variable_name in ("SECRET_KEY", "OPENAI_API_KEY", "PAGESPEED_API_KEY"):
            with self.subTest(variable_name=variable_name):
                environment = self._preflight_environment()
                environment["SECRET_KEY_SECRET_NAME"] = "test-django-secret"
                environment[variable_name] = ""
                result = self._run_preflight(environment)
                output = f"{result.stdout}\n{result.stderr}"
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("no puede enviarse como variable plana", output)
                self.assertNotIn("Construyendo imagen", output)

    def test_valid_secret_reference_passes_without_gcloud_or_build(self):
        environment = self._preflight_environment()
        environment["SECRET_KEY_SECRET_NAME"] = "test-django-secret"
        result = self._run_preflight(environment)
        output = f"{result.stdout}\n{result.stderr}"
        self.assertEqual(result.returncode, 0, output)
        self.assertIn("preflight valido", output)
        self.assertNotIn("Construyendo imagen", output)
        self.assertNotIn("gcloud", output.lower())

    def test_deploy_source_never_adds_secret_payloads_to_plain_environment(self):
        deploy = (REPOSITORY_ROOT / "deploy.sh").read_text(encoding="utf-8")
        self.assertNotIn('env_spec="${env_spec}|SECRET_KEY=${SECRET_KEY}"', deploy)
        self.assertNotIn('env_spec="${env_spec}|${secret_env}=${!secret_env}"', deploy)
        self.assertIn('secret_pairs=("SECRET_KEY=${SECRET_KEY_SECRET_NAME}:latest")', deploy)
        self.assertIn('--update-secrets "${secret_spec}"', deploy)


class ApprovedDependencyVersionTests(SimpleTestCase):
    def test_django_approved_security_release_is_installed_and_declared(self):
        requirements = (REPOSITORY_ROOT / "requirements.txt").read_text(encoding="utf-8")
        self.assertIn("Django==5.2.16", requirements.splitlines())
        self.assertEqual(django.get_version(), "5.2.16")
