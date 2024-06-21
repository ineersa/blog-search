from typing import List, Union, IO, Sequence, Any

from langchain_community.document_loaders.unstructured import UnstructuredFileIOLoader


class UnstructuredMarkdownFileIOLoader(UnstructuredFileIOLoader):
    """Load `Markdown` files using `Unstructured`.

    You can run the loader in one of two modes: "single" and "elements".
    If you use "single" mode, the document will be returned as a single
    langchain Document object. If you use "elements" mode, the unstructured
    library will split the document into elements such as Title and NarrativeText.
    You can pass in additional unstructured kwargs after mode to apply
    different unstructured settings.

    Examples
    --------
    from langchain_community.document_loaders import UnstructuredFileIOLoader

    with open("example.pdf", "rb") as f:
        loader = UnstructuredFileIOLoader(
            f, mode="elements", strategy="fast",
        )
        docs = loader.load()

    file = io.StringIO(text)
    document = UnstructuredMarkdownFileIOLoader(file_like_object, mode="elements", strategy="fast")

    References
    ----------
    https://github.com/Unstructured-IO/unstructured/blob/main/unstructured/partition/md.py
    """

    def __init__(
            self,
            file: Union[IO, Sequence[IO]],
            mode: str = "single",
            **unstructured_kwargs: Any,
    ):
        """Initialize with file path."""
        self.file = file
        super().__init__(file=file, mode=mode, **unstructured_kwargs)

    def _get_metadata(self) -> dict:
        return {}

    def _get_elements(self) -> List:
        from unstructured.__version__ import __version__ as __unstructured_version__
        from unstructured.partition.md import partition_md

        # NOTE(MthwRobinson) - enables the loader to work when you're using pre-release
        # versions of unstructured like 0.4.17-dev1
        _unstructured_version = __unstructured_version__.split("-")[0]
        unstructured_version = tuple([int(x) for x in _unstructured_version.split(".")])

        if unstructured_version < (0, 4, 16):
            raise ValueError(
                f"You are on unstructured version {__unstructured_version__}. "
                "Partitioning markdown files is only supported in unstructured>=0.4.16."
            )

        return partition_md(file=self.file, **self.unstructured_kwargs)
