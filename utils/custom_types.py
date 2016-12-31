from typing import Any, Dict, List, NewType, Union

JsonDict = Dict[str, Union[Dict[str, Any], List[Any], str, float, bool, None]]
HtmlStr = NewType('HtmlStr', str)
MarkdownStr = NewType('MarkdownStr', str)

