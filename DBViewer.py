import idaapi
import idc
import json

class DBViewer(idaapi.simplecustviewer_t):
    def Create(self, sn=None):
        # Form the title
        title = "DBViewer"
        if sn:
            title += " %d" % sn
        
        # Create the customview
        if not idaapi.simplecustviewer_t.Create(self, title):
            return False
            
        self.lines = []
        return True
        
    def to_line(self, db_entry):
        if type(db_entry) in (str, unicode):
            return str(db_entry)
        result = ''
        for idx, field in enumerate(db_entry):
            if type(field) in (int, long):
                result += '0x%08x' % (field)
            else:
                result += str(field)
            if idx < len(db_entry) - 1:
                result += ' '
        return result
        
    def load_db(self, db):
        self.lines = []
        self.ClearLines()
        for e in db:
            l = self.to_line(e)
            self.lines.append(l)
            self.AddLine(l)
        self.Refresh()
        
    def load(self, path):
        with open(path) as fp:
            db = json.load(fp)
        self.load_db(db)
        
    def save(self, path):
        with open(path, 'w') as fp:
            json.dump(self.lines, fp)
        
    def OnKeydown(self, vkey, shift):
        # ESCAPE?
        if vkey == 27:
            self.Close()
        #ENTER
        elif vkey == ord('\r'):
            ea = self.GetCurrentWord()
            try:
                ea = int(ea, base=0)
                idc.Jump(ea)
            except:
                print("Cannot jump to '%s'" % (ea))
        elif vkey == ord('G'):
            #add line
            n = self.GetLineNo()
            if n is not None:
                v = idc.AskLong(n, "Where to go?")
                if v:
                    self.Jump(v)
        elif vkey == ord('E'):
            idx = self.GetLineNo()
            if idx is not None:
                l = self.lines[idx]
                new_l = idc.AskStr(l, 'Insert line:')
                if new_l is not None:
                    self.lines[idx] = new_l
                    self.EditLine(idx, new_l)
                    self.Refresh()
        elif vkey == ord('L'):
            #load
            path = idaapi.ask_file(0, '*.json', 'Insert lines source')
            self.load(path)
        elif vkey == ord('S'):
            #save
            #for_saving = 1
            path = idaapi.ask_file(1, '*.json', 'Insert json path to save db to')
            self.save(path)
        else:
            return False
        return True

view = DBViewer()
if view.Create(1):
    view.Show()