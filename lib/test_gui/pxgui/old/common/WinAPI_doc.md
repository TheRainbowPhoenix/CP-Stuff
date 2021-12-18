# CreateWindowEx

### dwExStyle
Specifies the extended style of the window. This parameter can be one of the following values:

| Style       | Meaning      |
|:------------|--------------|
| WS_EX_ACCEPTFILES  | Specifies that a window created with this style accepts drag-drop files. | 
| WS_EX_APPWINDOW  | Forces a top-level window onto the taskbar when the window is minimized. |
| WS_EX_CLIENTEDGE  | Specifies that a window has a border with a sunken edge. | 
| WS_EX_CONTEXTHELP | Includes a question mark in the title bar of the window. When the user clicks the question mark, the cursor changes to a question mark with a pointer. If the user then clicks a child window, the child receives a WM_HELP message. The child window should pass the message to the parent window procedure, which should call the WinHelp function using the HELP_WM_HELP command. The Help application displays a pop-up window that typically contains help for the child window. WS_EX_CONTEXTHELP cannot be used with the WS_MAXIMIZEBOX or WS_MINIMIZEBOX styles. | 
|  WS_EX_CONTROLPARENT | Allows the user to navigate among the child windows of the window by using the TAB key. | 
| WS_EX_DLGMODALFRAME | Creates a window that has a double border; the window can, optionally, be created with a title bar by specifying the WS_CAPTION style in the dwStyle parameter. | 
|  WS_EX_LEFT | Window has generic "left-aligned" properties. This is the default. | 
| WS_EX_LEFTSCROLLBAR | If the shell language is Hebrew, Arabic, or another language that supports reading order alignment, the vertical scroll bar (if present) is to the left of the client area. For other languages, the style is ignored and not treated as an error. | 
| WS_EX_LTRREADING | The window text is displayed using Left to Right reading-order properties. This is the default. | 
| WS_EX_MDICHILD | Creates an MDI child window. | 
| WS_EX_NOPARENTNOTIFY | Specifies that a child window created with this style does not send the WM_PARENTNOTIFY message to its parent window when it is created or destroyed. | 
| WS_EX_OVERLAPPEDWINDOW | Combines the WS_EX_CLIENTEDGE and WS_EX_WINDOWEDGE styles. | 
| WS_EX_PALETTEWINDOW | Combines the WS_EX_WINDOWEDGE, WS_EX_TOOLWINDOW, and WS_EX_TOPMOST styles. | 
| WS_EX_RIGHT | Window has generic "right-aligned" properties. This depends on the window class. This style has an effect only if the shell language is Hebrew, Arabic, or another language that supports reading order alignment; otherwise, the style is ignored and not treated as an error. | 
| WS_EX_RIGHTSCROLLBAR | Vertical scroll bar (if present) is to the right of the client area. This is the default. | 
| WS_EX_RTLREADING | If the shell language is Hebrew, Arabic, or another language that supports reading order alignment, the window text is displayed using Right to Left reading-order properties. For other languages, the style is ignored and not treated as an error. | 
| WS_EX_STATICEDGE | Creates a window with a three-dimensional border style intended to be used for items that do not accept user input. | 
| WS_EX_TOOLWINDOW | Creates a tool window; that is, a window intended to be used as a floating toolbar. A tool window has a title bar that is shorter than a normal title bar, and the window title is drawn using a smaller font. A tool window does not appear in the taskbar or in the dialog that appears when the user presses ALT+TAB. | 
| WS_EX_TOPMOST | Specifies that a window created with this style should be placed above all non-topmost windows and should stay above them, even when the window is deactivated. To add or remove this style, use the SetWindowPos function. | 
| WS_EX_TRANSPARENT | Specifies that a window created with this style is to be transparent. That is, any windows that are beneath the window are not obscured by the window. A window created with this style receives WM_PAINT messages only after all sibling windows beneath it have been updated. | 
| WS_EX_WINDOWEDGE | Specifies that a window has a border with a raised edge. |