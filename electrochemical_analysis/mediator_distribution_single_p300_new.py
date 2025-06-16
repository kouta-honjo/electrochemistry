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
    
    #Solutions
    DM=reservoir['A1']
    DMG=reservoir['A2']
    
    #Each mediator is on the tuberack
    #In case for splitting from reservoir
    Mediator=[]
    for lane in ['A','B']:
        for num in range(1,7):
            Mediator.append(tubelack[lane+str(num)])
    
    # Wells for Mediator
    Wells=[plate['A'+str(x)] for x in range(1,13)]
    
    
    #######Distibution########
    
    # Distribute DM
    ctx.comment('Distribute DM')#P200のtip1の1列目は下2行
    p300_multi.pick_up_tip(tiprack_multi[0]['A1'])
    for i in range(len(Wells)):
        p300_multi.aspirate(150,DM)
        p300_multi.dispense(150,Wells[i].top(),rate=0.78)
        p300_multi.blow_out()
        p300_multi.touch_tip(speed=40,v_offset=-1, radius=0.6)
    p300_multi.drop_tip()
    
    # Distribute DMG
    ctx.comment('Distribute DMG')#P200のtip1の2列目は上6行
    p300_multi.pick_up_tip(tiprack_multi[0]['A2'])
    for i in range(12):
        p300_multi.aspirate(50,DMG)
        p300_multi.dispense(50,Wells[i].top(),rate=0.78)
        p300_multi.blow_out()
        p300_multi.touch_tip(speed=40,v_offset=-1, radius=0.6)
    p300_multi.drop_tip()
    
    # Distribute mediators
    ctx.comment('Distribute mediators')
    for i in range(len(Mediator)):
        p300_single.pick_up_tip()
        for alphabet in range(65,73):
            p300_single.mix(10,75,Mediator[i])
            p300_single.aspirate(50,Mediator[i])
            p300_single.dispense(50,plate[chr(alphabet)+str(i+1)].top())
            p300_single.blow_out()
            p300_single.touch_tip(speed=40,v_offset=-1, radius=0.6)
        p300_single.drop_tip()
    
    #Mixing
    for i in range(len(Wells)):
        p300_multi.pick_up_tip(tiprack_multi[1]['A'+str(i+1)])#P200のtip2
        p300_multi.mix(15,75,Wells[i])
        p300_multi.blow_out()
        p300_multi.drop_tip()