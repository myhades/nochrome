#!/usr/bin/env python3
"""Restore Vivaldi's existing menu component in its macOS address toolbar.

Version-specific, fails closed if the reviewed render expression changes.
Original application resource is backed up outside the repository.
"""
import argparse
import hashlib
from pathlib import Path
import shutil

VERSION = '8.2.4133.52'
OLD = 'children:[!T.ZP.isRTL()&&i,false,this.state.buttons.map'
NEW = 'children:[!T.ZP.isRTL()&&i,this.props.name===P.kToolbarsNavigation&&(0,Hi.jsx)(NW,{keyAccess:this.props.keyAccess,inert:!!this.props.inert,position:"mainbar",isHidden:!1}),this.state.buttons.map'

REQUEST_OLD = '_requestMenu(){this.hasMenu||K.Z.requestNamedMenu(EW)}'
REQUEST_NEW = '_requestMenu(){K.Z.requestNamedMenu(EW)}'

SHOW_OLD = '_showMenu=e=>{const t=this.refButton.current?.getBoundingClientRect();'
SHOW_NEW = '_showMenu=e=>{if(!this._getMenuItems(!0).length){this._pendingMenu=e;this._requestMenu();return}const t=this.refButton.current?.getBoundingClientRect();'
EVENT_OLD = 'case"menu":this.hasMenu=!0,this._setupShortcuts(!1);break;case"shortcut":this._setupShortcuts(!1),this._setButtonKeyshortcut()'
EVENT_NEW = 'case"menu":this.hasMenu=!0,this._setupShortcuts(!1);if(void 0!==this._pendingMenu&&this._getMenuItems(!0).length){const e=this._pendingMenu;this._pendingMenu=void 0;this._showMenu(e)}break;case"shortcut":this._setupShortcuts(!1),this._setButtonKeyshortcut()'

POPUP_OLD = '_W.show(this.context,s.id,[s],"bottom",this._onMenuStateChange)'
POPUP_INTERMEDIATE = '(0,Xs.Z)(this.context,n,e=>this._onMenuStateChange(e?0:-1),"bottomRight",this.refButton.current)()'
POPUP_NEW = '(0,Xs.Z)(this.context,n,e=>this._onMenuStateChange(e?0:-1),"pointer")({clientX:t.right,clientY:t.bottom,nativeEvent:{},persist(){},preventDefault(){},stopPropagation(){}})'

def transform(source):
    source = source.replace(POPUP_INTERMEDIATE, POPUP_OLD)
    for old, new in [(OLD, NEW), (REQUEST_OLD, REQUEST_NEW), (SHOW_OLD, SHOW_NEW), (EVENT_OLD, EVENT_NEW), (POPUP_OLD, POPUP_NEW)]:
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
        if source.count(NEW) != 1:
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
    print('Installed native menu component patch:', VERSION)
    print('Original SHA256:', hashlib.sha256(backup.read_bytes()).hexdigest())
    print('Backup:', backup)
    print('Restart Vivaldi to load it.')

if __name__ == '__main__':
    main()
