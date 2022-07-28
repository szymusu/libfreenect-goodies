import freenect

ctx = freenect.init()
print(ctx)
# device = freenect.open_device(ctx, 0)
# print(device)

depth, random_int = freenect.sync_get_depth()

print(len(depth))
print(len(depth[0]))

input("paused...")
freenect.sync_stop()