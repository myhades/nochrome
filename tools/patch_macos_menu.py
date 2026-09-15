#!/usr/bin/env python3
"""Add a Chrome-shaped application menu to Vivaldi's macOS toolbar.

Version-specific, fails closed if the reviewed render expression changes.
Original application resource is backed up outside the repository.
"""
import argparse
import hashlib
from pathlib import Path
import shutil

VERSION = '8.2.4133.52'
OLD = 'children:[!T.ZP.isRTL()&&i,false,this.state.buttons.map'
NEW = 'children:[!T.ZP.isRTL()&&i,this.props.name===P.kToolbarsNavigation&&(0,Hi.jsx)(ncChromeMenu,{keyAccess:this.props.keyAccess,inert:!!this.props.inert}),this.state.buttons.map'

CLASS_ANCHOR = 'const NW=(0,$i.Z)(kW,IW),ZW=Object.freeze'
CLASS_SOURCE = '''class ncChromeMenu extends Wi.PureComponent{static contextType=Yi.Z;root=Wi.createRef();state={open:!1};componentDidMount(){this.context.document.addEventListener("pointerdown",this._outside,!0)}componentWillUnmount(){this.context.document.removeEventListener("pointerdown",this._outside,!0)}_outside=e=>{this.state.open&&!this.root.current?.contains(e.target)&&this.setState({open:!1})};_toggle=e=>{e.preventDefault(),e.stopPropagation(),this.setState((e=>({open:!e.open})))};_run=e=>{this.setState({open:!1}),K.Z.executeActions("event",this.context,e)};_key=e=>{"Escape"===e.key&&(this.setState({open:!1}),e.preventDefault(),e.stopPropagation())};_item=(e,t,n)=>(0,Hi.jsxs)("button",{type:"button",role:"menuitem",className:"nc-menu-item",onClick:()=>this._run(t),children:[(0,Hi.jsx)("span",{children:e}),n&&(0,Hi.jsx)("kbd",{children:n})]});_sep=()=>(0,Hi.jsx)("div",{className:"nc-menu-separator",role:"separator"});render(){return(0,Hi.jsxs)("div",{className:"nc-chrome-menu-root",ref:this.root,onKeyDown:this._key,children:[(0,Hi.jsx)("button",{type:"button",className:"ToolbarButton-Button nc-chrome-menu-button",title:"Menu",tabIndex:this.props.keyAccess,inert:this.props.inert,"data-name":"ChromeMenu","aria-label":"Menu","aria-haspopup":"menu","aria-expanded":this.state.open,onMouseDown:this._toggle}),this.state.open&&(0,Hi.jsxs)("div",{className:"nc-chrome-menu-popup",role:"menu",children:[this._item("New tab","COMMAND_NEW_TAB","⌘T"),this._item("New window","COMMAND_NEW_WINDOW","⌘N"),this._item("New private window","COMMAND_NEW_PRIVATE_WINDOW","⇧⌘N"),this._sep(),this._item("History","COMMAND_SHOW_HISTORY","⌘Y"),this._item("Downloads","COMMAND_SHOW_DOWNLOADS","⇧⌘J"),this._item("Bookmarks","COMMAND_SHOW_BOOKMARKS"),this._item("Extensions","COMMAND_SHOW_EXTENSIONS"),this._item("Delete browsing data","COMMAND_SHOW_CLEAR_PRIVATE_DATA"),this._sep(),(0,Hi.jsxs)("div",{className:"nc-menu-zoom",children:[(0,Hi.jsx)("span",{children:"Zoom"}),(0,Hi.jsx)("button",{type:"button",title:"Zoom out",onClick:()=>this._run("COMMAND_MAIN_ZOOM_OUT"),children:"−"}),(0,Hi.jsx)("button",{type:"button",className:"nc-menu-zoom-reset",onClick:()=>this._run("COMMAND_MAIN_ZOOM_RESET"),children:"100%"}),(0,Hi.jsx)("button",{type:"button",title:"Zoom in",onClick:()=>this._run("COMMAND_MAIN_ZOOM_IN"),children:"+"}),(0,Hi.jsx)("button",{type:"button",title:"Full screen",onClick:()=>this._run("COMMAND_FULLSCREEN"),children:"⛶"})]}),this._item("Print","COMMAND_PRINT_PAGE","⌘P"),this._item("Find","COMMAND_FIND_IN_PAGE","⌘F"),this._item("Save page as","COMMAND_SAVE_PAGE","⌘S"),this._sep(),this._item("Developer tools","COMMAND_DEVELOPER_TOOLS","⌥⌘I"),this._item("Task manager","COMMAND_TASK_MANAGER"),this._item("View source","COMMAND_TAB_VIEW_PAGE_SOURCE"),this._sep(),this._item("Help","COMMAND_SHOW_HELP"),this._item("Settings","COMMAND_SHOW_SETTINGS")]})]})}}const NW=(0,$i.Z)(kW,IW),ZW=Object.freeze'''

DOWNLOAD_STATE_OLD = 'state={downloadProgress:0,isPopupVisible:!1};'
DOWNLOAD_STATE_NEW = 'state={downloadProgress:0,isPopupVisible:!1,showChromeButton:!1,hadActiveDownload:!1};hideChromeTimer=null;'
DOWNLOAD_MOUNT_OLD = 'componentDidMount(){this.props.inEditor||(hy.ZP.addListener(this._onDownloadStoreChange),Ui.Z.addListener("COMMAND_SHOW_DOWNLOADS_POPOUT",this.onCommandSpy))}'
DOWNLOAD_MOUNT_NEW = 'componentDidMount(){this.props.inEditor||(hy.ZP.addListener(this._onDownloadStoreChange),Ui.Z.addListener("COMMAND_SHOW_DOWNLOADS_POPOUT",this.onCommandSpy),globalThis.chrome?.downloads?.onCreated.addListener(this._onChromeDownloadCreated),globalThis.chrome?.downloads?.onChanged.addListener(this._onChromeDownloadChanged),this._refreshChromeDownloads())}'
DOWNLOAD_UNMOUNT_OLD = 'componentWillUnmount(){this.props.inEditor||(hy.ZP.removeListener(this._onDownloadStoreChange),Ui.Z.removeListener("COMMAND_SHOW_DOWNLOADS_POPOUT",this.onCommandSpy))}'
DOWNLOAD_UNMOUNT_NEW = 'componentWillUnmount(){this.hideChromeTimer&&clearTimeout(this.hideChromeTimer),this.props.inEditor||(hy.ZP.removeListener(this._onDownloadStoreChange),Ui.Z.removeListener("COMMAND_SHOW_DOWNLOADS_POPOUT",this.onCommandSpy),globalThis.chrome?.downloads?.onCreated.removeListener(this._onChromeDownloadCreated),globalThis.chrome?.downloads?.onChanged.removeListener(this._onChromeDownloadChanged))}'
DOWNLOAD_CHANGE_OLD = '_onDownloadStoreChange=()=>{this.setState({downloadProgress:hy.ZP.getTotalProgress()})};'
DOWNLOAD_CHANGE_NEW = '_refreshChromeDownloads=()=>globalThis.chrome?.downloads?.search({limit:100,orderBy:["-startTime"]},this._onRecentChromeDownloads);_onRecentChromeDownloads=e=>{const t=(e||[]).some((e=>"in_progress"===e.state)),n=Math.max(...(e||[]).map((e=>new Date(e.endTime||0).getTime())).filter(Number.isFinite)),i=n+36e5-Date.now();this.hideChromeTimer&&clearTimeout(this.hideChromeTimer),t?this.setState({showChromeButton:!0,hadActiveDownload:!0}):Number.isFinite(n)&&i>0?(this.setState({showChromeButton:!0,hadActiveDownload:!1}),this.hideChromeTimer=setTimeout((()=>this.setState({showChromeButton:!1,hadActiveDownload:!1})),i)):this.setState({showChromeButton:!1,hadActiveDownload:!1})};_onChromeDownloadCreated=e=>{this.setState({showChromeButton:!0,hadActiveDownload:!0}),this._refreshChromeDownloads()};_onChromeDownloadChanged=e=>{this._refreshChromeDownloads()};_onDownloadStoreChange=()=>{const e=hy.ZP.getTotalProgress();e?(this.hideChromeTimer&&clearTimeout(this.hideChromeTimer),this.setState({downloadProgress:e,showChromeButton:!0,hadActiveDownload:!0})):this.setState({downloadProgress:0},this._refreshChromeDownloads)};'
DOWNLOAD_HIDDEN_OLD = 'isHidden:this.props.isHidden,children:(0,Hi.jsx)(mz'
DOWNLOAD_HIDDEN_NEW = 'className:this.state.showChromeButton?"nc-download-visible":"nc-download-hidden",isHidden:this.props.isHidden,children:(0,Hi.jsx)(mz'
TOOLTIP_DELAY_OLD = 'appearDelay:(0,rz.Yt)(this.props.prefValues[P.kAutoHideEnabled])&&this.props.prefValues[P.kAutoHideTabBar]?600:200'
TOOLTIP_DELAY_NEW = 'appearDelay:e.style.width>=240?1300:Math.round(300+500*Math.log(Math.max(1,e.style.width-31))/Math.log(209))'
TAB_SCROLL_OLD = 'isHorizontalScrollingEnabled=()=>this.props.prefValues[P.kTabsHorizontalScrolling]&&("top"===this.props.tabPosition||"bottom"===this.props.tabPosition)'
TAB_SCROLL_NEW = 'isHorizontalScrollingEnabled=()=>!1'
TAB_SCROLL_LAYOUT_OLD = 'const i=r[P.kTabsHorizontalScrolling];let s;return'
TAB_SCROLL_LAYOUT_NEW = 'const i=!1;let s;return'
TAB_WIDTHS_OLD = 'gAe=180,bAe=150,fAe=30'
TAB_WIDTHS_NEW = 'gAe=240,bAe=150,fAe=32'
TAB_MIN_WIDTHS_OLD = 'minWidth:t||e||i?s:0,flexBasis:t?u:e?s:fAe'
TAB_MIN_WIDTHS_NEW = 'minWidth:t?u:e?Math.max(s||0,56):32,flexBasis:t?u:e?Math.max(s||0,56):32'
TAB_SPRING_OLD = 'OAe={stiffness:600,damping:36,precision:1}'
TAB_SPRING_PRIOR = 'OAe={stiffness:600,damping:50,precision:1}'
TAB_SPRING_PORT_V1 = 'OAe={stiffness:1200,damping:70,precision:1}'
TAB_SPRING_PORT_V2 = 'OAe={stiffness:1000,damping:63,precision:2}'
TAB_LINEAR_PORT_V1 = 'OAe={stiffness:-1,damping:200,precision:.01}'
TAB_SPRING_NEW = 'OAe={stiffness:-1,damping:150,precision:.01}'
SPRING_INTEGRATOR_OLD = 'function tP(e,t,n,i,s,a,o){const r=n+(-s*(t-i)+-a*n)*e,l=t+r*e;return Math.abs(r)<o&&Math.abs(l-i)<o?(eP[0]=i,eP[1]=0,eP):(eP[0]=l,eP[1]=r,eP)}'
SPRING_INTEGRATOR_NEW = 'function tP(e,t,n,i,s,a,o){if(-1===s){(0===n||n*(i-t)<=0)&&(n=(i-t)/(a/1e3));const s=t+n*e;return n>0&&s>=i||n<0&&s<=i||Math.abs(s-i)<o?(eP[0]=i,eP[1]=0,eP):(eP[0]=s,eP[1]=n,eP)}const r=n+(-s*(t-i)+-a*n)*e,l=t+r*e;return Math.abs(r)<o&&Math.abs(l-i)<o?(eP[0]=i,eP[1]=0,eP):(eP[0]=l,eP[1]=r,eP)}'
TAB_CLOSE_ANIMATION_OLD = 'this.setState({animate:!1},(()=>{this.props.closePage(i).then((()=>{this.allowDelayedAnimation()}))}))'
TAB_CLOSE_ANIMATION_NEW = 'this.setState({animate:!0},(()=>{this.props.closePage(i)}))'
TAB_CLOSE_FREEZE_OLD = '!e.pinned&&this.props.prefValues[P.kTabsAlignNext]&&e.id!==this.props.tabs.last()?.id&&this.freezeTabSize(e)'
TAB_CLOSE_FREEZE_NEW = '!e.pinned&&e.id!==this.props.tabs.last()?.id&&this.freezeTabSize(e)'
TAB_CLOSE_TOOLTIP_OLD = 'onMouseDown:i,title:a})'
TAB_CLOSE_TOOLTIP_NEW = 'onMouseDown:i,"aria-label":a})'
TAB_LEAVE_METHOD_OLD = 'getStyles=()=>{const{tabs:e,maxWidth:t,maxHeight:n}=this.props'
TAB_LEAVE_METHOD_NEW = 'getLeaveStyle=e=>this.#Hn&&"tab"===e.data?.type?{...e.style,width:VP(18,OAe)}:null;getStyles=()=>{const{tabs:e,maxWidth:t,maxHeight:n}=this.props'
TAB_LEAVE_RENDER_OLD = '(0,Hi.jsx)(oAe,{styles:t,children:e=>this.#ei(e,s,a,n)})'
TAB_LEAVE_RENDER_NEW = '(0,Hi.jsx)(oAe,{styles:t,willLeave:this.getLeaveStyle,children:e=>this.#ei(e,s,a,n)})'
TAB_LAYOUT_RESERVE_OLD = 'const o=this.createFlexBoxLayout(e,t,n,{pageIdsHiddenForDrag:'
TAB_LAYOUT_RESERVE_NEW = 'const o=this.createFlexBoxLayout(e,this.#Hn?Math.max(0,t-20):t,n,{pageIdsHiddenForDrag:'
TAB_OPEN_GEOMETRY_OLD = 'this.context.requestAnimationFrame((()=>{this.#f&&this.forceUpdate()})),this.#Un=e.map((e=>e.key));const t=e.map((e=>({...e,style:{...e.style,width:0}})));return this.#Fn=r,[...s,...t]'
TAB_OPEN_GEOMETRY_PORT_V1 = 'this.context.requestAnimationFrame((()=>{this.#f&&this.forceUpdate()})),this.#Un=e.map((e=>e.key));const t=e.map((e=>({...e,style:{...e.style,width:18}})));return this.#Fn=r,[...s,...t]'
TAB_OPEN_GEOMETRY_BAD = 'this.context.requestAnimationFrame((()=>{this.#f&&this.forceUpdate()})),const t=Math.max(0,...s.filter((e=>"tab"===e.data?.type)).map((e=>vAe(e.style.x)+vAe(e.style.width))));this.#Un=e.map((e=>e.key));const n=e.map((e=>({...e,style:{...e.style,x:Math.max(vAe(e.style.x),t-18),width:18}})));return this.#Fn=r,[...s,...n]'
TAB_OPEN_GEOMETRY_NEW = 'this.context.requestAnimationFrame((()=>{this.#f&&this.forceUpdate()}));const t=Math.max(0,...s.filter((e=>"tab"===e.data?.type)).map((e=>vAe(e.style.x)+vAe(e.style.width))));this.#Un=e.map((e=>e.key));const n=e.map((e=>({...e,style:{...e.style,x:Math.max(vAe(e.style.x),t-18),width:18}})));return this.#Fn=r,[...s,...n]'
TAB_OPEN_SECOND_FRAME_OLD = 'if(this.#Hn&&this.#Un.length){const e=this.#Un;this.#Un=[];const t=r.map((t=>e.includes(t.key)?{...t,style:{...t.style,x:vAe(t.style.x)}}:t));return this.#Fn=t,t}'
TAB_OPEN_SECOND_FRAME_NEW = 'if(this.#Hn&&this.#Un.length)return this.#Un=[],this.#Fn=r,r;'

def transform(source):
    # Migrate bundles patched by an earlier port revision before applying the
    # reviewed original-to-current substitutions below.
    for prior_spring in (TAB_SPRING_PRIOR, TAB_SPRING_PORT_V1, TAB_SPRING_PORT_V2, TAB_LINEAR_PORT_V1):
        if source.count(prior_spring) == 1 and source.count(TAB_SPRING_NEW) == 0:
            source = source.replace(prior_spring, TAB_SPRING_NEW, 1)
    if source.count(TAB_OPEN_GEOMETRY_BAD) == 1 and source.count(TAB_OPEN_GEOMETRY_NEW) == 0:
        source = source.replace(TAB_OPEN_GEOMETRY_BAD, TAB_OPEN_GEOMETRY_NEW, 1)
    if source.count(TAB_OPEN_GEOMETRY_PORT_V1) == 1 and source.count(TAB_OPEN_GEOMETRY_NEW) == 0:
        source = source.replace(TAB_OPEN_GEOMETRY_PORT_V1, TAB_OPEN_GEOMETRY_NEW, 1)
    pairs = [
        (OLD, NEW),
        (CLASS_ANCHOR, CLASS_SOURCE),
        (DOWNLOAD_STATE_OLD, DOWNLOAD_STATE_NEW),
        (DOWNLOAD_MOUNT_OLD, DOWNLOAD_MOUNT_NEW),
        (DOWNLOAD_UNMOUNT_OLD, DOWNLOAD_UNMOUNT_NEW),
        (DOWNLOAD_CHANGE_OLD, DOWNLOAD_CHANGE_NEW),
        (DOWNLOAD_HIDDEN_OLD, DOWNLOAD_HIDDEN_NEW),
        (TOOLTIP_DELAY_OLD, TOOLTIP_DELAY_NEW),
        (TAB_SCROLL_OLD, TAB_SCROLL_NEW),
        (TAB_SCROLL_LAYOUT_OLD, TAB_SCROLL_LAYOUT_NEW),
        (TAB_WIDTHS_OLD, TAB_WIDTHS_NEW),
        (TAB_MIN_WIDTHS_OLD, TAB_MIN_WIDTHS_NEW),
        (SPRING_INTEGRATOR_OLD, SPRING_INTEGRATOR_NEW),
        (TAB_SPRING_OLD, TAB_SPRING_NEW),
        (TAB_CLOSE_ANIMATION_OLD, TAB_CLOSE_ANIMATION_NEW),
        (TAB_CLOSE_FREEZE_OLD, TAB_CLOSE_FREEZE_NEW),
        (TAB_CLOSE_TOOLTIP_OLD, TAB_CLOSE_TOOLTIP_NEW),
        (TAB_LEAVE_METHOD_OLD, TAB_LEAVE_METHOD_NEW),
        (TAB_LEAVE_RENDER_OLD, TAB_LEAVE_RENDER_NEW),
        (TAB_LAYOUT_RESERVE_OLD, TAB_LAYOUT_RESERVE_NEW),
        (TAB_OPEN_GEOMETRY_OLD, TAB_OPEN_GEOMETRY_NEW),
        (TAB_OPEN_SECOND_FRAME_OLD, TAB_OPEN_SECOND_FRAME_NEW),
    ]
    for old, new in pairs:
        if source.count(new) == 1:
            continue
        if source.count(old) != 1:
            raise ValueError('Expected exactly one reviewed expression; refusing to patch.')
        source = source.replace(old, new, 1)
    return source

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--restore', action='store_true')
    parser.add_argument('--app', type=Path, default=Path('/Applications/Vivaldi.app'))
    args = parser.parse_args()
    resource = args.app / f'Contents/Frameworks/Vivaldi Framework.framework/Versions/{VERSION}/Resources/vivaldi/bundle.js'
    source = resource.read_text()
    backup_dir = Path.home() / 'Library/Application Support/noChrome/backups' / VERSION
    backup = backup_dir / 'bundle.js'
    if args.restore:
        if source.count(NEW) != 1 or source.count(CLASS_SOURCE) != 1:
            raise ValueError('Installed resource is not the expected patched version.')
        original = backup.read_text()
        if transform(original) != source:
            raise ValueError('Resource changed since installation; refusing to overwrite it.')
        resource.write_text(original)
        print('Restored original menu resource. Restart Vivaldi.')
        return
    result = transform(source)
    if result == source:
        print('Menu patch already installed.')
        return
    backup_dir.mkdir(parents=True, exist_ok=True)
    if backup.exists() and transform(backup.read_text()) != result:
        raise ValueError('Existing backup differs; refusing to overwrite it.')
    if not backup.exists():
        shutil.copy2(resource, backup)
    resource.write_text(result)
    print('Installed Chrome-style toolbar menu patch:', VERSION)
    print('Original SHA256:', hashlib.sha256(backup.read_bytes()).hexdigest())
    print('Backup:', backup)
    print('Restart Vivaldi to load it.')

if __name__ == '__main__':
    main()
