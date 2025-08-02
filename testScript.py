import sys
print("sys.executable:", sys.executable)
print("sys.version:", sys.version.replace('\n',' '))
try:
    import cst.interface
    print("Imported cst.interface OK")
except Exception as e:
    print("Failed to import cst.interface:", e)
