import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Any, Callable, Generic, Iterable, TypeVar


logger = logging.getLogger(__name__)


T = TypeVar("T")
JSONDict = dict[str, Any]


class StorageError(Exception):
    """Raised when a storage operation fails."""
    

class JSONStorage(Generic[T]):
    """
    Generic JSON-based storage.

    This class is responsible only for:
    - Managing the storage path
    - Reading JSON data
    - Writing JSON data
    - Performing atomic writes
    - Raising storage-related errors

    It does NOT know anything about Book, Member, Borrowing, etc.
    """

    def __init__(
        self,
        file_name: str,
        data_dir: Path | None = None,
    ) -> None:

        self.data_dir = (
            data_dir
            if data_dir is not None
            else Path(__file__).resolve().parent.parent / "data"
        )

        self._validate_file_name(file_name)

        self.file_path = self.data_dir / file_name

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save_all(
        self,
        items: Iterable[T],
        serializer: Callable[[T], JSONDict],
    ) -> None:
        """
        Convert Python objects to JSON-compatible dictionaries
        and save them to the JSON file.
        """

        try:
            json_data = [
                serializer(item)
                for item in items
            ]

            self._atomic_write(json_data)

        except (OSError, TypeError, ValueError) as exc:
            logger.exception(
                "Failed to save JSON data to %s",
                self.file_path,
            )

            raise StorageError(
                f"Failed to save data to {self.file_path}"
            ) from exc

    def load_all(
        self,
        deserializer: Callable[[JSONDict], T],
    ) -> list[T]:
        """
        Load JSON data from the file and convert each dictionary
        back into a Python object.
        """

        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                raw_data = json.load(file)

            if not isinstance(raw_data, list):
                raise StorageError(
                    f"Invalid data format in {self.file_path}: "
                    "expected a list"
                )

            for item in raw_data:
                if not isinstance(item, dict):
                    raise StorageError(
                        f"Invalid item in {self.file_path}: "
                        "expected an object"
                    )

            return [
                deserializer(item)
                for item in raw_data
            ]

        except json.JSONDecodeError as exc:
            logger.exception(
                "Invalid JSON format in %s",
                self.file_path,
            )

            raise StorageError(
                f"Invalid JSON format in {self.file_path}"
            ) from exc

        except OSError as exc:
            logger.exception(
                "Failed to read %s",
                self.file_path,
            )

            raise StorageError(
                f"Failed to read {self.file_path}"
            ) from exc

    def _atomic_write(self, data: Any) -> None:
        """
        Safely write data using a temporary file and then replace
        the original file.

        This prevents the main JSON file from being left partially
        written if the process fails during writing.
        """

        temporary_path: Path | None = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.file_path.parent,
                delete=False,
            ) as temp_file:

                json.dump(
                    data,
                    temp_file,
                    indent=4,
                    ensure_ascii=False,
                )

                temp_file.flush()
                os.fsync(temp_file.fileno())

                temporary_path = Path(temp_file.name)

            os.replace(
                temporary_path,
                self.file_path,
            )

            temporary_path = None

        finally:
            if (
                temporary_path is not None
                and temporary_path.exists()
            ):
                try:
                    temporary_path.unlink()
                except OSError:
                    pass

    @staticmethod
    def _validate_file_name(file_name: str) -> None:
        """
        Validate that the provided file name is a safe JSON file name.
        """

        path = Path(file_name)

        if path.is_absolute():
            raise ValueError(
                "file_name must be a relative path"
            )

        if ".." in path.parts:
            raise ValueError(
                "file_name cannot contain '..'"
            )

        if path.suffix.lower() != ".json":
            raise ValueError(
                "file_name must have a .json extension"
            )