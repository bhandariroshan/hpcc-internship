subscription = 'us-hpccplatform-dev'
subscription_id = 'ec0ba952-4ae9-4f69-b61c-4b96ff470038'
resource_prefix = 'roshan-test-'

n_threads = 5

image = "UbuntuLTS"
priority = "Spot"
max_price = "0.00001"
eviction_policy = "Deallocate"

region_codes = [
    'eastus',
    'westus',
    'japaneast',
    'southindia',
    'centralindia',
    'ukwest',
    'germanywestcentral',
    'eastasia',
    'brazilsouth',
    'canadacentral',
    'australiaeast'
]


sizes = [
    "Standard_A4m_v2",        # 4 vCPU, 32 Gb Ram
    "Standard_A8_v2",         # 8 vCPU, 16 Gb Ram
    "Standard_NC8as_T4_v3",    # 8   56 GiB"
    "Standard_NV6s_v2",
    "Standard_H8m",
    "Standard_D4a_v4",        # 4   16 GiB  100 GiB
    "Standard_D8a_v4",        # 8   32 GiB  200 GiB
    "Standard_D4as_v4",       # 4   16 GiB  32 GiB
    "Standard_D8as_v4",       # 8   32 GiB  64 GiB
    "Standard_D8ds_v5",       # 8   32 GiB  300 GiB 
    "Standard_D2_v3",         # 2   8 GiB   50 GiB
    "Standard_D4_v3",         # 4   16 GiB  100 GiB
    "Standard_D8_v3",         # 8   32 GiB  200 GiB
    "Standard_DS3_v2",        # 4   14 GiB  28 GiB
    "Standard_F4s_v2",        # 4   8 GiB   32 GiB
    "Standard_F8s_v2",        # 8   16 GiB  64 GiB
    "Standard_F4",            # 4   8 GiB   64 GiB
    "Standard_F8",            # 8   16 GiB  128 GiB  
    "Standard_E4ds_v5",        # 4   32 GiB  150 GiB
    "Standard_E8ds_v5",       # 8   64 GiB  300 GiB
    "Standard_E2s_v3",        # 2   16 GiB  32 GiB
    "Standard_E4s_v3",        # 4   32 GiB  64 GiB  
    "Standard_E8s_v3",        # 8   64 GiB  128 GiB
    "Standard_NC6s_v3",       # 6   56 GiB  340 GiB
    "Standard_NC12s_v3",      # 12  112 GiB 680 GiB
    "Standard_NC4as_T4_v3",   # 4   28 GiB  180 GiB"
    "Standard_NV12s_v2",
    "Standard_H8",
    "Standard_H16"
]

resource_names = [resource_prefix + location for location in region_codes]