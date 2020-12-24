import os
import re
import subprocess
import sys
from typing import List

from docker_tools import code_timeout, docker_image_name
from docker_tools.docker_exception import DockerException


class CodeRunner:
	"""
	Used to create docker environments and use them to run Python scripts in a safe and consistent environment
	"""
	def __init__(self):
		"""
		Default constructor sets filename and requried packages to default values
		"""
		self.filename = None
		self.requried_packages = set()
		self.files = set()

	def set_filename(self, filename: str) -> None:
		"""
		Sets stored filename

		Args:
			filename (str): filename in
		"""
		self.filename = filename

	def add_package(self, package_name: str) -> None:
		"""
		Adds a package that will be installed when dockerfile is generated

		Args:
			package_name (str): name of package to be added by pip command
		"""
		self.requried_packages.add(package_name)

	def add_file(self, filename: str) -> None:
		"""
		Adds a file to be copied to the docker instance

		Args:
			filename (str): Name of the file to be copied
		"""
		self.files.add(filename)

	def run(self, cleanup: bool = False, include_exit_code: bool = False) -> str:
		"""
		Runs a python file in a docker environment without any extra arguments

		Args:
			cleanup (bool): delete all related docker images when finished
			include_exit_code (bool): include process exit code in return string

		Returns:
			str: the stdout and stderr of running the given python script in a string
		"""
		return self.run_args([], cleanup=cleanup, include_exit_code=include_exit_code)

	def run_args(self, argv: List[str], cleanup: bool = False, include_exit_code: bool = False) -> str:
		"""
		Runs a pythong file in a docker environment with arguments

		Args:
			argv (List[str]): an array of arguments to pass to the python script run
			cleanup (bool): delete all related docker images when finished
			include_exit_code (bool): include process exit code in return string

		Returns:
			str: the stdout and stderr of running the given python scfript in a string

		Raises:
			DockerException: No filename has been set
			FileNotFoundError: The specified filename does not exist
		"""
		if self.filename is None:
			raise DockerException('Filename not set')
		if not os.path.exists(self.filename):
			raise FileNotFoundError('Could not find file to run in docker')
		self._generate_docker_context()
		try:
			output = 'EXIT CODE: 0\n' if include_exit_code else ''
			output += subprocess.check_output(['docker', 'run', '-it', '--rm', cfg.docker_image_name] + argv, stderr=subprocess.STDOUT, timeout=code_timeout).decode('utf-8')
		except subprocess.CalledProcessError as e:
			output = f'EXIT CODE: {e.returncode}\n' if include_exit_code else ''
			output += f'{e.output.decode("utf-8")}'
		if cleanup:
			delete_docker_images()
		return output

	def _generate_docker_context(self) -> str:
		"""
		Generates an appropiate dockerfile and the runs it to create a docker image. Will add the python packages
		and copy the files that have been specified.

		Returns:
			str: The id of the context created

		Raises:
			DockerException: Error creating the docker context
			FileNotFoundException: Could not find a file that was supposed to be copied over
		"""
		dockerfile = open('dockerfile', 'w')
		dockerfile.writelines(['FROM python:3\n',
		                       'WORKDIR /usr/src/app\n',
		                       f'COPY {self.filename} {self.filename}\n',
		                       f'CMD ["{self.filename}"]\n'])
		for file in self.files:
			if not os.path.exists(file):
				raise FileNotFoundError(f'Could not find {file} to copy to docker instance')
			dockerfile.writelines([f'COPY {file} {file}\n'])
		if len(self.requried_packages) > 0:
			dockerfile.writelines([f'RUN pip install {" ".join(self.requried_packages)}\n'])
		dockerfile.writelines([f'ENTRYPOINT ["python3", "./{self.filename}"]\n'])
		dockerfile.close()
		output = subprocess.check_output(['docker', 'build', '-t', docker_image_name, '.']).decode('utf-8')
		context_id = re.search(r'Successfully built (.+)\n', output)[0]
		if context_id is None:
			raise DockerException('Could not create docker context')
		return context_id


def delete_docker_images() -> None:
	"""
	Deletes all docker images related to this project
	"""
	print(f'WARNING: deleting {cfg.docker_image_name} docker images', file=sys.stderr)
	subprocess.run(['docker', 'system', 'prune', f'-label={docker_image_name}', '-f'], stdout=open(os.devnull, 'wb'))
