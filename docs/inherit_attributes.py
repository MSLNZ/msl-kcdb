"""Custom mkdocs extension to inherit the `Attributes:` section of the base class."""  # noqa: INP001

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from griffe import DocstringSectionKind, Extension

if TYPE_CHECKING:
    from griffe import DocstringAttribute, GriffeLoader, Module, Object


def _inherit_attributes(obj: Object) -> None:  # noqa: C901
    if obj.is_module:
        for member in obj.members.values():
            if not member.is_alias:
                _inherit_attributes(member)  # type: ignore[arg-type]

    if obj.is_class:
        parent_attributes: list[DocstringAttribute] = []
        for parent in obj.mro():  # type: ignore[attr-defined]
            if parent.docstring is not None:
                for section in parent.docstring.parsed:
                    if section.kind is DocstringSectionKind.attributes:
                        parent_attributes.extend(section.value)

        if obj.docstring is not None:
            for section in obj.docstring.parsed:
                if section.kind is DocstringSectionKind.attributes:
                    section_names = [s.name for s in section.value]
                    section.value.extend(pa for pa in parent_attributes if pa.name not in section_names)
                    section.value.sort(key=lambda x: x.name)


class InheritAttributes(Extension):
    """Custom mkdocs extension to inherit the `Attributes:` section of the base class."""

    def on_package_loaded(self, *, pkg: Module, loader: GriffeLoader, **kwargs: Any) -> None:  # noqa: ANN401, ARG002
        """Inherit the Attributes section from parent classes after the whole package is loaded."""
        return _inherit_attributes(pkg)
