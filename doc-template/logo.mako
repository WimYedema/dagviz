<%
  from pdoc.html_helpers import format_git_link
  from pathlib import Path
  mpath = Path(format_git_link("{path}", module)).parts
  root = mpath[0:-1]
  api = mpath[1:-1]
  toRoot = "../"*len(root)
  toApi = "../"*len(api)
%>
<a href="./${toRoot}index.html">DAGVIZ</a> &ndash; <a href="./${toApi}index.html">API</a>
