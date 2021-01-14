import idc
import sark

def fix_noret_line(ea=None):
    """Fix lines that calls to functions that created by IDA as noret func"""
    if not ea:
        ea = idc.here()
    idc.force_bl_call(ea)
    
def fix_noret_func(func=None):
    """Fix function that was created as noret func"""
    if not func:
        func = sark.Function()
    if func.is_noret:
        new_flags = func.flags ^ idaapi.FUNC_NORET
        idc.set_func_flags(func.ea, new_flags)

def get_struct_offset(s):
    """Get offset in struct for expressions like 'gap12[72]'"""
    h, d = s.replace('gap', '').split(']')[0].split('[')
    h = int(h, base=16)
    d = int(d)
    return hex(h + d)
