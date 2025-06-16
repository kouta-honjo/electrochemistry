def get_values(*names):
    import json
    _all_values = json.loads("""{"p300_mount_single":"right","p300_mount_multi":"left","tip_type_single":"opentrons_96_tiprack_300ul","tip_type_multi":"opentrons_96_tiprack_300ul","plate_type":"watson_96_wellplate_330ul","reservoir_type":"ssibio_12_reservoir_1100ul"}""")
    return [_all_values[n] for n in names]

metadata = {
    'protocolName': 'Mediator',
    'author': 'Takashi Fujikawa <FUJIKAWA.Takashi@nims.go.jp>',
    'description': 'Preparation for mediators experiment',
    'apiLevel': '2.9'
}

def run(ctx):
    #tip type
    [p300_mount_single, p300_mount_multi, tip_type_single, tip_type_multi, plate_type, reservoir_type] = get_values(  # noqa: F821
    "p300_mount_single", "p300_mount_multi", "tip_type_single", "tip_type_multi", "plate_type", "reservoir_type")
    
    # Load Labware
    tiprack_single = ctx.load_labware(tip_type_single, 7)
    tiprack_multi1 = ctx.load_labware(tip_type_multi, 8)
    tiprack_multi2 = ctx.load_labware(tip_type_multi, 9)
    
    tiprack_single = [tiprack_single]
    tiprack_multi = [tiprack_multi1,tiprack_multi2]
    plate = ctx.load_labware(plate_type, 1)
    reservoir= ctx.load_labware(reservoir_type,2)
    tubelack = ctx.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',3)
    
    # Load Pipette
    p300_single = ctx.load_instrument('p300_single_gen2', p300_mount_single, tip_racks=tiprack_single)
    p300_multi = ctx.load_instrument('p300_multi_gen2', p300_mount_multi, tip_racks=tiprack_multi)
  
    
    #Each substrate is on the tuberack
    #In case for splitting from reservoir
    Substrate=[chr(x//6+65)+str(x%6+1) for x in range(24)]
    
    
    # Wells for Mediator
    #Wells=[plate['A'+str(x)] for x in range(1,13)]
    
    
    #######Distibution########
    
    # Distribute substrate
    ctx.comment('Distribute substrate')#P200のtip1の1列目は下2行
    p300_single.pick_up_tip()
    for i in range(96): 
	p300_single.mix(10,75,tuberack[substrate[i//4]])
        p300_single.aspirate(100,tuberack[substrate[i//4]])
	p300_single.dispense(100,plate[chr(int(i//12)+65)+str(int(i%12)+1)].top(),rate=0.78)
	p300_single.touch_tip(speed=40,v_offset=-1, radius=0.6)


	
    
   