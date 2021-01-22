from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Type, List

from loguru import logger

if TYPE_CHECKING:
    from MSPACompiler.tags.baseTag import BaseTag


class Macro:
    """Create alternative name for user created tag
    """
    @staticmethod
    def process(
            data: Dict[str, List[Dict[str, str]]],
            base_tag: Type[BaseTag],
            temp_tags: Dict[str, Type[BaseTag]] = None
    ):
        """Create alternative name for user created tag

        Parameters
        ----------
        data : `Dict[str, List[Dict[str, str]]]`
            Dictionary containg list of dictionaries. Key is new name, value
            is name if an existing tag

        base_tag : `Type[BaseTag]`
            BaseTag to which the alias will belong

        temp_tags : `Dict[str, Type[BaseTag]]`, optional
            If specified, alias will be awailable temporarily,
            by default `None`
        """
        if not (data['args']):
            return

        for i in data['args']:
            for new, old in i.items():
                new, old = new.lower(), old.lower()

                if temp_tags is not None:
                    dst = temp_tags
                    if old in temp_tags:
                        src = temp_tags
                    else:
                        src = base_tag.tags
                else:
                    dst = base_tag.tags
                    src = base_tag.tags

                if not (new and old) or new in dst:
                    if not old:
                        logger.info(
                            'Missing name of the tag, that the alias will '
                            'belong'
                        )
                    if new in dst:
                        logger.info(
                            f'Tag/macro with name {new} already exists. '
                            'Skipping...'
                        )
                    continue

                tag = src.get(old)
                if tag:
                    dst[new] = tag
