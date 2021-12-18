LASTRESULT = None


def function_299(local_number1, local_string1, local_string2, local_number2) -> int:
    try:
        local_number2 = (local_number1 <= 0)
        if (local_number2):
            print(local_number2)



def function_296():
    pass



def function_417():
    pass


def UseDll(dll_name):
    print(f"USE DLL {dll_name}")


def inx_MyFunction(local_number1: int):
    local_number2: int = 9999
    local_number3: int = 9999
    local_number4: int = 9999
    local_number5: int = 9999

    local_string1: str = "changeMe"
    local_string2: str = "changeMe"
    local_string3: str = "changeMe"

    function_299(local_number1, "SUPPORTDIR", local_string1, local_number2)
    function_296(local_number1)
    local_number4 = LASTRESULT
    local_string3 = (local_string1 + "OSUpdateDll.dll")
    local_string2 = local_string1
    function_417(local_string2)
    UseDll(local_string3)
    local_number3 = LASTRESULT

    print(f"OSUpdate ({local_number4}, 0, {repr(local_string2)})")
    local_number5 = LASTRESULT
    print(f"UnUseDll({local_string3})")