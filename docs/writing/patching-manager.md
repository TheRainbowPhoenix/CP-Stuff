# Patching the CP-Manager
Let's try to change some text on the CPM ROM and see how it goes !

## Background
I'm a software engineer that enjoy low-level understanding, and I'm learning retro-engineering during my free time.
All the tools presented here may be imperfect, but I'm working with what I know. Feels free to contact me if you want to discuss or recommend anything ! 

## Needed tools
I'm using mostly free/open source tools since I want this to be accessible to anyone who's interested in RE.

I'd recommend using :
- [Cutter](https://cutter.re), IDA-like RE with Ghidra plugin
- [PEBear](https://hshrzd.wordpress.com/pe-bear/), A quick tool for [Windows PE](https://en.wikipedia.org/wiki/Portable_Executable) analysis and editing
- [x86DBG](https://x64dbg.com/), a cool windows debugger that is able to rewrite ASM at runtime

Optional but interesting for investigation :
- [DllExp](https://www.nirsoft.net/utils/dll_export_viewer.html), a tool helping to see the DLL exports
- [SysInternals' ProcMon](https://docs.microsoft.com/en-us/sysinternals/downloads/procmon) used for monitoring opened file and reg key, also give the callStack
- [SysInternals' ProcExp](https://docs.microsoft.com/en-us/sysinternals/downloads/process-explorer) used for process tree viewing and finding the launch command and environment
- [ApiMonitor](http://www.rohitab.com/apimonitor), a tool to see the dll call and the parameters. It's sadly not maintained since 2013, so if you know better tool I'll happily use it !
- [Resource Hacker](http://www.angusj.com/resourcehacker/) used for PE resource editing (like icon and stuff)
- [LessMSI](https://github.com/activescott/lessmsi) used for MSI extracting
- [7zip](https://www.7-zip.org/download.html), that's able t extract a lot of file format and even PE !
- [Notepad++](https://notepad-plus-plus.org/downloads/), a text editor capable of large file handling

Also my favorite programming language, that I use a lot for scripting :
- [Python](https://www.python.org/downloads/) with the cool `ctype` for dll communication. I use it as PoC and testings.

## First step
As a conscientious dev, I prefer launch exe into a VM. I use HyperV on my machine but [VirtualBox](https://www.virtualbox.org/) or [VMWare](https://www.vmware.com/products/workstation-player.html) also works.
It's a bit out of context, so I consider you already have a Windows VM. You can get free Windows 10 trial ISO with [Evaluation center](https://www.microsoft.com/en-us/evalcenter/evaluate-windows-10-enterprise) or even a [VagrantBOX](https://app.vagrantup.com/gusztavvargadr/boxes/windows-10).

I would also advice you to cut the VM internet connexion, since the exe downloaded from Internet may do evil things. From my first studies, their licensing system is from a company that I know make data-collecting-hungry license manager so better not give them too much :D  

Now it's running, get the CPManager ! I got the "CPM Subscription for CPII Ver 2.00.4" since it's the easiest to patch (Yes, the DRM one)

![cp23_sub_2004000_2a.zip](https://media.discordapp.net/attachments/874327340577062973/874327838008954880/unknown.png)

Extract it, we get a single `.exe`. For my knowledge, this icon means it's an [InstallShield](https://en.wikipedia.org/wiki/InstallShield) installer.
The easiest way to get the [MSI](https://en.wikipedia.org/wiki/Windows_Installer) from it is simply to launch it !

### Extracting the files

Using [ProcMon](#Needed_tools), we can see the following :

![ProcMon shows CPM and Msiexec](https://media.discordapp.net/attachments/874327340577062973/874330102211686430/unknown.png)

By clicking the "msiexec.exe" subprocess, we can see some interesting details like the launch command :

![Launch command of Msiexec](https://media.discordapp.net/attachments/874327340577062973/874330293824278638/unknown.png)

It's possible to "Select all `Ctrl-A`", "Copy `Ctrl-C`" and then paste it to a notepad.
We may get something similar :
```
MSIEXEC.EXE /i "C:\Users\vagrant\AppData\Local\Downloaded Installations\{2D2A3442-10AA-448C-B0FC-7A88AC2CAB32}\ClassPadManagerSubscriptionforClassPad II.msi"  TRANSFORMS="C:\Users\vagrant\AppData\Local\Temp\{16653C26-5027-4816-8011-7D8EAA46D5F6}\1033.MST" SETUPEXEDIR="C:\Users\vagrant\Downloads\cp2m_sub_2004000_2a" SETUPEXENAME="ClassPad Manager Subscription for ClassPad II Ver. 2.00.4000.exe"
```

The interesting part is the msi path, located in `%localappdata%\Downloaded Installations\{2D2A3442-10AA-448C-B0FC-7A88AC2CAB32}`. Let's open this folder and copy the MSI for later !

I copied it to my "Downloads" folder, where I usually put random stuff. Using lessMSI, it's possible to get all the files inside of the msi :

![LessMSI extracted the MSI](https://media.discordapp.net/attachments/874327340577062973/874385152111935528/unknown.png)

Simply fire "Extract" to a folder of your choice and enjoy all the files of the MSI !

### Understanding the files

Once you're done extracting, a folder called "SourceDir" has been created, containing a lot of junk.

The "SourceDir" folder directly contains some dll and a mysterious `.tlb` file but none of them matters. 
It's possible to get dll information using `right clic > properties` and going to `Details`. Doing so will tell you that this DLL are "Microsoft OLE".
For short, OLE (Object Linking and Embedding) is a windows technology used when a program want to embed some files. 
Even if they're not in use, it's possible to know a bit more about the dll using [DllEXP]. Simply click cancel on the "first load" prompt and drag your dll onto it :

![DllExp some dll](https://media.discordapp.net/attachments/874327340577062973/874390650341171200/unknown.png)

Okay so it's plain Microsoft DLL, nothing more. The `.tlb` is a bit suspicious if you aren't familiar with Windows95. It was used in the same manner as DLL.
A quick way to find this out is opening the file with Notepad++ and looking at the headers :

![TLB file headers](https://cdn.discordapp.com/attachments/874327340577062973/874392002710605834/unknown.png)

The windows Executable (PE) contains the `MZ` two first bytes, and generally contains the `This program cannot be run in DOS mode.` a bit after because of legacy.
If you see that on a file, there's a high chance it's an exe or a DLL.
You can try to perform some analysis with PEBear to know what's inside but for now we won't because this file is simply the old OLE for Windows 95.

The Folder "Win" will be the files copied to "C:\Windows" if they don't exist. There, it's only files for [MFC](https://en.wikipedia.org/wiki/Microsoft_Foundation_Class_Library) compatibility and [runtime](https://en.wikipedia.org/wiki/Microsoft_Visual_C%2B%2B) ("msvcr" = MicroSoft VisualC++Runtime). It's safe to ignore it for now.

The next folder, "program files", is where the cool stuff begins ! This folder would be copied to "C:\Program Files\" and so its content is where the program actually sits.

## CPM Files

The "Licence" folder is only for demo licensing. After patching, we won't need it.

Moving to the real folder, we got the following files :

![CPM files](https://cdn.discordapp.com/attachments/874327340577062973/874394358584057896/unknown.png)

Here's a small list of what does what, from my first understanding :

|:File name      | Explained                     |
|----------------|-------------------------------|
| `ActivationFxMb` | Activation DLL, used to check and prompt for licensing |
| CPM.exe        | The main file, where to focus  |
| `*.duplicateN` | Files that got duplicated. Looks like the normal file is the japanese version, the `1` English and so on |
| `libcurl`      | A quick yet powerful way to do HTTP requests. |
| `libeay32`     | OpenSSL crypto libray. Used by `libcurl` |
| `MpLangRes`    | Transaltion file. One version per language |
| `ssleay32`     | OpenSSL SLL libray. Used by `libcurl` |
| `Physium.c2a`  | Physium Add-in used by the CPM and classpad |

Let's take a deeper look at the files. 

## Activation

When facing an unknown dll, it's almost automatic for me to drag and drop it to DLLExp. Let's do this !

![DLLExp for the Activation dll](https://cdn.discordapp.com/attachments/874327340577062973/874396533922099230/unknown.png)

Some really classic stuff going on here.
`GetInformation` should be responsible for user licensing infos,
`GetPrpertyPage` for [device fingerprinting](https://en.wikipedia.org/wiki/Device_fingerprint) ,
`IsActivationDialog` should be a function that displays the ActivationDialog and returns a boolean ("Is-" is a common prefix for boolean).

Finally, `SetInformation` and `SetInformationA` should be responsible for user info writing. Easy !

There're two ways to confirm that : **Dynamic analysis**, at runtime with <u>API monitor</u> and <u>x86dbg</u> and **static analysis** with <u>Cutter</u>.
For now, we'll go with static and launch cutter. Drag and drop the DLL to the "Open File" and press "Ok" on the "Load Options".

At first launch, you'd get a window like this :

![Cutter file dashboard](https://media.discordapp.net/attachments/874327340577062973/874407772404465724/unknown.png)

Here's my personal workflow that I use for most of the binaries

#### Strings analysis

Take a look at the strings, short them by "Length" or "Size" and scroll until you only got garbage. 
As you can read, the file itself is about licensing and activation. One funny thing to look at is the "pdb" file location. Even if we don't have access to it, we can guess a lot from its path. 
Here the pdb path is `F:\\Users\\{dev_name}\\開発\\VS2010\\Activation\\Release_Multibyte\\{dll_name}.pdb`. The internals told us that :
- They are using Visual Studio 2010
- The "Users" folder is generally where Windows is installed, so they may have windows on an external drive
- They are from Japan, because their folder name is `開発`: "development"

Search for strings with interesting content like "http", ".ini", ".exe" or "Software\\" :
- Their website uses an activation page called `lfa.php`
- Some links point to "EMS", which is a famous cloud-powered DRM. 
- The app stores his licensing info on an ini file
- Their internal DRM is called SE██T█NEL (Some parts are redacted for avoiding AI-grep monitoring). Take a look at it, it's really messy...

If you want to find where a string *may* be used, simply right click and "Show X-Refs" :

![Show X-Refs on string](https://cdn.discordapp.com/attachments/874327340577062973/874413281652138034/unknown.png)

You'd there get a window with detailed references and disasembled code corresponding :

![X-Refs for string and disasm](https://cdn.discordapp.com/attachments/874327340577062973/874413542760149034/unknown.png)

It's definitely possible to start from there and dig deeper. I'd recommend trying this when you don't know where to start but with a string.

> Note: Sometimes the X-refs won't find anything... Cutter is still in its early days but tries its best ! Try a deeper analysis mode or simply use another string ...

#### Imports analysis

Windows applications and DLL use functions from the Windows API. That way, they can integrate with the system. 

Here's some interesting imports :

`AdvAPI32` have some "advanced api" functions, like "[RegOpenKeyA](https://docs.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regopenkeya)" for registry keys reading. All of the windows functions are documented on the [Win32API Docs](https://docs.microsoft.com/en-us/windows/win32/api/).


`Kernel32` is the Windows kernel interface, with some functions like "[CreateFileA](https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea)" for file creating, "[CreateProcessA](https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa)" for process (like when you launch a .exe app) creation or even "[ReadFile](https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-readfile)" for file reading.

It also provide a very commonly used function called "[LoadLibrayA](https://docs.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-loadlibrarya)". I've a big love/hate relation with this functions, since it empowers the program DLL loading from their name. You guessed it, your program can load a DLL that isn't located in the "Import Table" we're looking at. When debugging, it's a reflex for me to debug their calls and see what's loaded. This is a really cool function too because it make us able to perform some "DLL Injection".
The principe is really simple : If the application want to load "CoolLibrary.dll", it'll first look in its directory and then browse other folders. Let's say you placed a merely identical dll to the one called but with some modifications to one of the called method ? Yeah, it executes them anyway ! Note that we can also do that with any DLL present in the folder, just prevent yourself from modifying the Windows DLL...

`MSVCR100` will provide some common C/C++ functions like "[atoi](https://www.cplusplus.com/reference/cstdlib/atoi)" , "[memcpy](https://www.cplusplus.com/reference/cstring/memcpy)", "[strcmp](https://www.cplusplus.com/reference/cstring/strcmp/)" and so on ... 

`User32` provide User-Interface related functions like "[MessageBoxA](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messageboxa)", used for alerts when something is wrong or user confirmation.

`WS2_32` is the interface to WinSock, the Windows way to do some socket (internet IP) requests. "[revc](https://docs.microsoft.com/en-us/windows/win32/api/winsock/nf-winsock-recv)" and "[setsockopt](https://docs.microsoft.com/en-us/windows/win32/api/winsock/nf-winsock-setsockopt)" are part of commonly used functions. This may means that the program is doing some IP request to a server.

`libCurl` is a way on quickly posting message to an HTTP/HTTPS website and getting responses. From the previously found strings, this may means that the app does some HTTP POST request to some website.

> A little side-note about the trailing "A" or "W" on functions: Windows got every function in both ASCII (A) mode or Unicode (W) mode

Now we got some basic background about DLL, let's use it to locate some code !
It's fairly easy to locate some asembly code using an import with "Show X-Refs" while selecting the dll name.
Doing so on the promising "LoadLibrayA" will show something like this :

![LoadLibrayA X-refs](https://cdn.discordapp.com/attachments/874327340577062973/874427098519990392/unknown.png)

The second entry here is really easy to understand so we'll use it as demo :

```assembly
0x1001d75e      push    str.Iphlpapi.dll ; 0x10096cdc ; LPCSTR lpLibFileName
0x1001d763      call    dword [LoadLibraryA] ; 0x10095168 ; HMODULE LoadLibraryA(LPCSTR lpLibFileName)
```

Really simple ! The code try to load the "Iphlpapi.dll" dll, used for [IP Helper](https://docs.microsoft.com/en-us/windows/win32/api/iphlpapi/)

> Pro tip: If you want to look up some dll without getting polluted by the "Download DLL" scams, write "dllName win32" or "dllName winapi" (without the .dll)

The third one is pretty similar :

```assembly
0x10023370      push    str.wsock32.dll ; 0x100970f0
0x10023375      call    dword [LoadLibraryA] ; 0x10095168 ; HMODULE LoadLibraryA(LPCSTR lpLibFileName)
```

From my understanding it try to call `WS2_32` function and if it fails, it'll try to load the legacy winsock dll. Let's check using dissaembly :

![View Full Disassembly](https://cdn.discordapp.com/attachments/874327340577062973/874428523085975562/unknown.png)

Thanks to the jump indicator, it's easier to understand :

![Full Disassembly with jump arrows](https://cdn.discordapp.com/attachments/874327340577062973/874429101258194994/unknown.png)

The function `fcn.100232a5` should determines if the program is on legacy windows or something  and then returns a code. This code is later tested, and the library load will change according to it
`je` means "Jump If". I'd recommend reading some [assembly manual](https://faydoc.tripod.com/cpu/je.htm) to have a better understanding of the functions. 
`push` will simply put in stack the string value, helpfully named as the string. 

We could easily get a C-like code using the Ghidra plugin to get a better understanding :

![Decompile function](https://cdn.discordapp.com/attachments/874327340577062973/874430213004607548/unknown.png)

The following code would be generated, confirming the idea of "version switch":

```cpp
iVar2 = fcn.100232a5();
if (iVar2 == 0) {
    pcVar3 = "wsock32.dll";
} else {
    pcVar3 = "ws2_32.dll";
}
```

Right after, we can see it recreating symbols from the DLL, like the following for the function "inet_addr" :

```cpp
*(int32_t *)0x100cf738 = (*_GetProcAddress)(*(int32_t *)0x100cf734, "inet_addr");
```

It's pretty easy to get to the lower function and continue investigations. Let's select the function before the condition and show it in "graph":

![Show function graph](https://cdn.discordapp.com/attachments/874327340577062973/874431727735541761/unknown.png)

And get the pretty graph :

![Pretty function graph](https://cdn.discordapp.com/attachments/874327340577062973/874432149883863070/unknown.png)

Some ASM-guy like this interface so much because it's halfway assembly block and give you a pretty good view on how the blocks works.

Reading it quickly (only the import and strings) make me understand that it checks for some "[GetVersionExA](https://docs.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-getversionexa)" to get the Windows version and then compares it to "5", which is code for Windows XP.   

#### Exports analysis

Since we're working with a DLL and not an Executable, dll usually have exported functions for the Exe to use.
We can monitor them using API Monitor, but for now we'll simply take a look at them.

On Cutter, choose "Windows" > "Info..." > "Exports" and simply show it in a new graph or disassembly.

![graph view](https://cdn.discordapp.com/attachments/874327340577062973/874443257059348490/unknown.png)

From there, it's possible to edit and update the code as you like. Let's for example remove some of the calls here.
First, I'd recommend you to copy the file to a backup location. Then, switch to "Cache mode" from the "File > Set mode" menu :

![Switch to cache mode](https://cdn.discordapp.com/attachments/874327340577062973/874443561486143518/unknown.png)

That way, you'll be able to "Commit changes" when you're done !

Let's try for example to remove the function call here. You have the "nop" instruction in asm that simply "do nothing".

Choose from the right clic menu "Edit > Nop Instruction"

![Nop Instruction](https://cdn.discordapp.com/attachments/874327340577062973/874444307455684648/unknown.png)

That way, you'd get something like this ! Cool !

![graph view](https://cdn.discordapp.com/attachments/874327340577062973/874442677033259058/unknown.png)

You can also manually imput it using the "Edit > Instruction"

![Edit Instruction](https://cdn.discordapp.com/attachments/874327340577062973/874444669206032414/unknown.png)

So far so good ! Let's move to some more complicated example !

## The CP Manager
This file is a bit huge for a "regular" exe. It's better to take a look at its content from PE-Bear:

![PEBear of the exe](https://cdn.discordapp.com/attachments/874327340577062973/874446074474025000/unknown.png)

The blue part is the ".text" where the code sits, the green part on the right is the ".rdata" part where resource binaries are stocked, and the red part is the ".rsrc" where the icons and other resources are stocked.

Before extracting I'd like to talk a bit about [BinVis.io](https://BinVis.io). This tool is a great way to visualise your file. 

By default, the tool will display the bytes classes :

![ByteClass infos](https://cdn.discordapp.com/attachments/874327340577062973/874447433562738688/unknown.png)

Let's open the .exe with it :

![BinVis of byte class](https://cdn.discordapp.com/attachments/874327340577062973/874447081891328060/706c364f-18cb-4439-978b-6219b7f795a1.png)

Basically we can understand that :
- Red or mixed blue/red mean code
- Blue mean human-readable text
- White is unused / empty space
- Black is padding 

Next, choose the brush and switch to "Entropy". This is a great way to find if the file is compressed :

![Entropy Mode](https://cdn.discordapp.com/attachments/874327340577062973/874448205985759263/unknown.png)

Here's, for reference, how to read the generated picture :

![Entropy infos](https://cdn.discordapp.com/attachments/874327340577062973/874448496604889169/unknown.png)

And the generated map of the file :

![Entropy of the file](https://cdn.discordapp.com/attachments/874327340577062973/874448459061657620/acdf98a9-b3ea-4391-8723-d549b70f44e4.png)

From this, we guess than except the bright part, nothing is compressed. Entropy is a way to tell if bytes change a lot, which is generally true when compressing data.

With this informations, we can try to extract the sections with PEBear :

![Save rdata from PEBear](https://cdn.discordapp.com/attachments/874327340577062973/874449772885442560/unknown.png)

As I already extracted all the sections and looked into them, the rom is located in the .rdata and isn't even compressed ! Great !

### Visualizing the ROM

I made a little script in python that'll help us visualising the rom content! Crunchy stuff ahead !

To use it, you'll need to install numpy and pillow. Here's the command to install it :
`pip install pillow numpy`

```python
from PIL import Image
import numpy as np
f = open("cpm/.rdata", "rb")
l = f.read()
f.close()

MASK5 = 0b011111
MASK6 = 0b111111

while len(l)%32 != 0:
    l += b'\x00'

dt = np.dtype(np.uint16)
# # Uncomment this if you're viewing the SH4 rom and not the CPM one
# dt = dt.newbyteorder('>')

im = np.frombuffer(l, dtype=dt)

b = (im & MASK5) << 3
g = ((im >> 5) & MASK6) << 2
r = ((im >> (5 + 6)) & MASK5) << 3

rgb = np.dstack((r,g,b)).astype(np.uint8)


mode = 'RGB'
xdim = 640
ydim = len(rgb[0]) // xdim

image = Image.frombytes('RGB', (xdim, ydim), rgb, 'raw')
image.show()
```

Here's the output I got : 

![ROM image](https://media.discordapp.net/attachments/874327340577062973/874451208998383696/unknown.png?width=111&height=935)
![Home screen buttons](https://cdn.discordapp.com/attachments/874327340577062973/874451602143084554/unknown.png)
As you can see, there's some graphical rom assets onto it !

Let's then have fun with our ROM !

You have the choice, you can either isolate the .rdata alone and work on it without touching the .exe or opening the cpm.exe and let Cutter do everything. For now, I'll open the full exe since it'll be easier to work on later.

### First h4x

Let's do something basic : Changing the "ALgy 2" to "Hook 2" text on home screen !
Go into the "Strings" section of Cutter and search for "Algy 2". Try to "X-Refs" the strings to find the one used.

I found it on the "Menu Button Text" list :

![Menu button text list](https://cdn.discordapp.com/attachments/874327340577062973/874453689778208829/unknown.png)

You can either open in on a new Graph or disassembly to take a deeper look at what's going on, or simply don't care and replace the text.
If you wish to dig a bit more in that direction, you'll find cool stuff like where "ini files" are writen with the parameters.

To keep things simple, let's just go back to strings and show the "Algy 2" in the hexdump :

![Show string in HexDump](https://cdn.discordapp.com/attachments/874327340577062973/874456923343323166/unknown.png)

Choose the option to "Edit > Write String" on the hexdump. Please note that your string have to be the exact same size or less than the original, or you'll create overflows.

![Edit Write String](https://cdn.discordapp.com/attachments/874327340577062973/874457229003210842/unknown.png)

If prompt, choose "Cache mode" which is safer.
Once done, apply "File > Commit changes" from the menu and simply launch it. If you have enabled algy (by droping the file in the right folder) you'll see the text changes

![Modified text in CPM](https://cdn.discordapp.com/attachments/874327340577062973/874458738277359676/unknown.png) 

Finally, take a moment to enjoy what we're doing ! Isn't it awesome ? Editing code that simply !

> After messing a bit with the code and modifying it, I'd recommand to keep a backup of every patch you did. That way, It'll be easier to undo changes and get back to a working version.
 
# Dynamic analysis

So yeah now you want to understand how it work in a more detailed level ? No problems !

## Looking at files 

Let's start ProcMon. When launching, you'll be prompted for rules. It's really important do define correct rules otherwise your pc will die from computing too much data.
Please save all your work before doing so and close all process-intensive applications.
A good-working rule for process is to limit "Image Path" "begins with" > The folder where your exe is. That way, only the .exe launched from this folder will be monitored.

![ProcMon rules](https://cdn.discordapp.com/attachments/874327340577062973/874459845112258611/unknown.png)

You can stop the monitoring any time by clicking the magnifier icon after the floppy icon.

![Sample output of ProcMon](https://cdn.discordapp.com/attachments/874327340577062973/874460643196026920/unknown.png)

You'll see the files and registry keys opened, but also eventual network requests.

Double-clicking on an entry will show the details :

![Operation details](https://cdn.discordapp.com/attachments/874327340577062973/874461467011866624/unknown.png)

From there we can see that the cpm seeked at the 93th character of the file and write one byte.

Notepad++ can help you seeing what have been wrote using the "Pos:" indicator :

![Pos Indicator showing 95](https://cdn.discordapp.com/attachments/874327340577062973/874462007569576067/unknown.png)

Yeah, it wrote "0" in the "VarPaletteOpen" option. You can even see what address of the function did that in the "Stack" tab on procmon event:

![Stack mode of ProcMon](https://cdn.discordapp.com/attachments/874327340577062973/874461552923791441/unknown.png)

Remember when we talked about "LoadLibraryA" ? You can also monitor this :

![LoadLibraryW](https://cdn.discordapp.com/attachments/874327340577062973/874462904458551356/unknown.png)

This tool can help you in many way, like finding where a game save is located or debugging why the dll won't load

## Exploring DLL function calls

Choose the "x86" version on API Monitor and launch it ! Click ok on the info and wait a bit for dependencies to load. Be sure to have checked all the "API Filter":

![API Filter all enabled](https://cdn.discordapp.com/attachments/874327340577062973/874463590009167902/unknown.png)

Choose "File > Monitor new Process" and locate the CPM exe. I'd recommend Attach using Remote Thread since the application seems to check directly for a debugger.

![Monitor Options](https://cdn.discordapp.com/attachments/874327340577062973/874464310447980674/unknown.png)

For my experience, it'll grow very fast in memory usage so better not use it for too long. Click "OK" to start and let the program run until it's fully loaded and choose "File > Pause monitoring" or simply close the application.

Expanding the "Module" tree, you'd be able to select some dll and filter to only watch them. Here's an example of the activation DLL :

![Activation DLL API calls](https://cdn.discordapp.com/attachments/874327340577062973/874467241876410388/unknown.png)

If you don't see anything maybe you missed the step where you have to check the "API Filter" boxes.
You sould see 'X of Y calls' on the top bar as shown in the picture.

Let's explain the panels quickly :
- "Parameters" is where you'd expect to see the dll function call with each parameters and their values. You can even copy them, really cool !
- "Call Stack" is the calling stack that triggered the API Call, it's really useful for later use in x86DBG or Cutter.
- "Hex Buffer" will provide a quick buffer view of the memory state
- "Output" is a debug log of the application.

With the dll call details, we could even try to call them from a python or C/C++ code using the exactly same logic : 
"LoadLibraryA" and recreating function name then calling them.

I won't go further into details here, since it's not really useful...

## Watching asm and modify it at runtime

Open "x86DBG" and choose "File > Open"
As soon as you open the cpm, it'll launch and pause it. It's really important to know where to look : At the bottom left you have the yellow square when the program is paused.
Using the "resume" option will resume its execution

![x86DBG launch screen](https://media.discordapp.net/attachments/874327340577062973/874468305879064576/unknown.png)

From the "Sylbols" tab, choose the cpm.exe and filter (using the bottom bar) for "LoadLibrary" calls. Add a BreakPoint using right click > "Toggle Breakpoint"

![Add Breakpoint to LoadLibrary](https://cdn.discordapp.com/attachments/874327340577062973/874470920218103808/unknown.png)

You can then resume using the "=>" arrow button icon right before the "Stop" squared icon or choose "Debug" > "Run" from menu.
The program will run until halting to a breakpoint
After stepping a bit, you'll see a lot of DLL have been loaded :

![Loaded DLL](https://cdn.discordapp.com/attachments/874327340577062973/874472182389026846/unknown.png)

I personally breaked at "IsActivationDialog" function from the Activation DLL since it's easy to understand and mess with.
Going back to the "CPU" tab, you'll see the execution halting. You can choose the "Step" option to carefully step to next operation
Since you're going to do a lot of "step over" and "Step Into", it's good to kown that F7 and F8 keys are for "Into" and "Over".

A very cool feature of x86DBG is "ASMJiT", a feature to rewrite asm at runtime. You can call it using right clic > Assemble:

![ASM Assemble](https://cdn.discordapp.com/attachments/874327340577062973/874473145317335080/unknown.png)

And then change it to whatever you want. Check "Fill with NOP's" if you want the line to do nothing :

![Edit asm line](https://cdn.discordapp.com/attachments/874327340577062973/874473453229580308/unknown.png)

![Replace with NOP](https://cdn.discordapp.com/attachments/874327340577062973/874473769102639155/unknown.png)

![View the result](https://cdn.discordapp.com/attachments/874327340577062973/874473930629464105/unknown.png)

Then congratulation, you NOP'd some instruction ! You can do whatever ASM you want, but you're always limited by the size.
As someone told me, you can choose the tricky option to "jmp somewhere empty" and there write your lovely code !

From there let's do something cool !
Go to the "Symbols" and locate the "User32.dll", then find the "MessageBoxA" and choose "Follow in Disassembler"

![Follow in DisAsm](https://cdn.discordapp.com/attachments/874327340577062973/874477243521466438/unknown.png)

Then, choose to copy the function address. It's really important since it'll allow you to call it somewhere else:

![Copy the MessageBoxA address](https://cdn.discordapp.com/attachments/874327340577062973/874477259103289414/unknown.png)

Then finally write some ASM using the "Assemble" option :

![ASM code](https://cdn.discordapp.com/attachments/874327340577062973/874477277981839430/unknown.png)

Basically there you push some options into the stack. 
```assembly
mov eax, esp
mov dword [eax + 0xc], 0x30  ; put the "MB_ICONWARNING" to the dialog
mov dword [eax + 8], 0x25BE4A8  ;  put some variable as Title
mov dword [eax + 4], 0x25BE4A8  ;  put some variable as text
mov dword [eax], 0  ; Handle to the parent window.
call 0x7668EA80  ; Call the MessageBoxA address you copied
```
Refer to the [MessageBoxA](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messageboxa) doc for more details about the parameters.

And that's it ... except I'm dumb and inserted an address that pointed nowhere

After steing after the call, should now see a MessageBox :

![MessageBox with invalid text](https://cdn.discordapp.com/attachments/874327340577062973/874477289910444083/unknown.png)

Okay now you understand what's a pointer : basically the address of a location, which can chang over time ! Let's use static location instead :
Go to the Memory Map and locate the .data section where the strings are stored. Right click on ".data" and choose "Follow in Dump".

![Locate .data](https://cdn.discordapp.com/attachments/874327340577062973/874484122008047646/unknown.png)

Scroll a bit until you find a string that please you and copy its address.

![Copy String address](https://cdn.discordapp.com/attachments/874327340577062973/874483883536711690/unknown.png)

I'll use the following strings for this:

| Address      | Text     |
|:-------------|----------|
| `0x01263424` | profit   |
| `0x012634A4` | MaxValue |

The corresponding asm then become :

```assembly
mov eax, esp
mov dword [eax + 0xc], 0x30  ; put the "MB_ICONWARNING" to the dialog
mov dword [eax + 8], 0x01263424  ;  put some variable as Title
mov dword [eax + 4], 0x012634A4  ;  put some variable as text
mov dword [eax], 0  ; Handle to the parent window.
call 0x7668EA80  ; Call the MessageBoxA address you copied
```

And then carefuly step into it :

![Stonks](https://cdn.discordapp.com/attachments/874327340577062973/874483855321600051/unknown.png)

Max Profit ! You've successfully modified runtime asm ! What to do next ? You could cold-apply changes to the binary in cutter and happily fix bugs in software !

