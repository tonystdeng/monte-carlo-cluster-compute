import os
import posixpath


def sftp_put_folder(sftp, simulationPath, destination):
    """
    Upload a file or directory recursively via Paramiko SFTP.

    Args:
        sftp: Paramiko SFTPClient
        simulationPath: Local file or directory path
        destination: Remote file or directory path
    """

    def mkdir_p(remote_dir):
        parts = []
        while remote_dir not in ("", "/"):
            parts.append(remote_dir)
            remote_dir = posixpath.dirname(remote_dir)

        for path in reversed(parts):
            try:
                sftp.stat(path)
            except FileNotFoundError:
                sftp.mkdir(path)

    # Single file
    if os.path.isfile(simulationPath):
        remote_parent = posixpath.dirname(destination)
        mkdir_p(remote_parent)
        sftp.put(simulationPath, destination)
        return

    # Directory
    if os.path.isdir(simulationPath):
        mkdir_p(destination)

        for root, dirs, files in os.walk(simulationPath):
            rel_path = os.path.relpath(root, simulationPath)

            remote_root = (
                destination
                if rel_path == "."
                else posixpath.join(destination, rel_path.replace(os.sep, "/"))
            )

            mkdir_p(remote_root)

            for file_name in files:
                local_file = os.path.join(root, file_name)
                remote_file = posixpath.join(remote_root, file_name)

                sftp.put(local_file, remote_file)

        return

    raise FileNotFoundError(f"Local path does not exist: {simulationPath}")