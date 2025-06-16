def get_values(*names):
    import json
    _all_values = json.loads("""{"p300_single_mount":"right","p300_multi_mount":"left","tip_type_single":"opentrons_96_tiprack_300ul","tip_type_multi":"opentrons_96_tiprack_300ul","plate_type":"watson_96_wellplate_330ul","reservoir_type":"bmbiost_12_reservoir_4000ul"}""")
    return [_all_values[n] for n in names]

metadata = {
    'Version': '1.0',
    'Date': '23/3/8',
    'protocolName': 'Serial dilution',
    'author': 'Takashi Fujikawa <FUJIKAWA.Takashi@nims.go.jp>',
    'description': 'Serial dilution for antibiotics exp.',
    'apiLevel': '2.9'
}

def run(ctx):
    #tip type
    [p300_single_mount, p300_multi_mount, tip_type_single, tip_type_multi, plate_type, reservoir_type] = get_values(  # noqa: F821
    "p300_single_mount", "p300_multi_mount", "tip_type_single", "tip_type_multi", "plate_type", "reservoir_type")
    
    # Load Labware
    plate_solution = ctx.load_labware(plate_type, 1)
    plate_dilution1 = ctx.load_labware(plate_type, 2)
    plate_dilution2 = ctx.load_labware(plate_type, 5)
    plate_dils=[plate_dilution1,plate_dilution2]
    plate_sample = ctx.load_labware(plate_type, 3)
    #tiprack_single = ctx.load_labware(tip_type_single, 7)
    tiprack_multi = ctx.load_labware(tip_type_multi, 8)
    
    
    ###Settings###
    
    #Load Pipette
    p300_single = ctx.load_instrument('p300_single_gen2', p300_single_mount, tip_racks=[tiprack_multi])
    p300_multi = ctx.load_instrument('p300_multi_gen2', p300_multi_mount, tip_racks=[tiprack_multi])
    
    #Wells for Dilution
    Wells_dilution=['A'+str(x) for x in range(1,13)]
    
    #Wells for start of dilution
    Wells_dil_start=['A1','A7']
    
    #Wells for Samples
    #Wells_sample=['A4','A5','A11','A12']
    Wells_sample=['A4','A5','A11']

    ###Working###
    
    #Preparation
    ctx.comment('Preparation of PBS')
    for i in range(len(plate_dils)):
        p300_multi.pick_up_tip()
        for t in range(len(Wells_dilution)):
            if t in [0,1,2,3]:
                p300_multi.move_to(plate_solution['A5'].bottom(z=3))
                p300_multi.aspirate(180,plate_solution['A5'])
                p300_multi.dispense(180,plate_dils[i][Wells_dilution[t]].top(),rate=0.78)
                p300_multi.blow_out()
                p300_multi.touch_tip(speed=40,v_offset=-1,radius=0.6)
            if t in [4,5]: 
                p300_multi.move_to(plate_solution['A5'].bottom(z=3))
                p300_multi.aspirate(150,plate_solution['A5'])
                p300_multi.dispense(150,plate_dils[i][Wells_dilution[t]].top(),rate=0.78)
                p300_multi.blow_out()
                p300_multi.touch_tip(speed=40,v_offset=-1,radius=0.6)
            if t in [6,7,8,9]:
                p300_multi.move_to(plate_solution['A5'].bottom(z=3))
                p300_multi.aspirate(180,plate_solution['A5'])
                p300_multi.dispense(180,plate_dils[i][Wells_dilution[t]].top(),rate=0.78)
                p300_multi.blow_out()
                p300_multi.touch_tip(speed=40,v_offset=-1,radius=0.6)
            if t in [10,11]:
                p300_multi.move_to(plate_solution['A5'].bottom(z=3))
                p300_multi.aspirate(150,plate_solution['A5'])
                p300_multi.dispense(150,plate_dils[i][Wells_dilution[t]].top(),rate=0.78)
                p300_multi.blow_out()
                p300_multi.touch_tip(speed=40,v_offset=-1,radius=0.6)

        p300_multi.drop_tip()
    
    #Pause#
    ctx.pause("Put the 96 electrode plate for samples on No.3")
    
    #Transfer
    ctx.comment('Transfer sample')
    for t in range(len(Wells_sample)):
        p300_multi.pick_up_tip()
        p300_multi.mix(15,100,plate_sample[Wells_sample[t]].bottom(z=3))
        p300_multi.aspirate(20,plate_sample[Wells_sample[t]].bottom(z=3))
        p300_multi.dispense(20,plate_dils[t//2][Wells_dil_start[t%2]].top(),rate=0.78)
        p300_multi.blow_out()
        #p300_multi.touch_tip(speed=40,v_offset=-1, radius=0.6)
        p300_multi.mix(15,100,plate_dils[t//2][Wells_dil_start[t%2]].bottom(z=3))
        p300_multi.drop_tip()
        
    #Serial Dilution
    ctx.comment('Serial Dilution')
    for s in range(len(plate_dils)):
        p300_multi.pick_up_tip()
        for i in range(len(Wells_dilution)-1):
            if i in [0,1,2]:
                p300_multi.move_to(plate_dils[s][Wells_dilution[i]].bottom(z=3))
                p300_multi.mix(3,150,plate_dils[s][Wells_dilution[i]].bottom(z=3),rate=2.0)
                p300_multi.aspirate(20,plate_dils[s][Wells_dilution[i]].bottom(z=3))
                p300_multi.dispense(20,plate_dils[s][Wells_dilution[i+1]].top(),rate=0.78)
                p300_multi.blow_out()
                p300_multi.mix(12,150,plate_dils[s][Wells_dilution[i+1]].bottom(z=3),rate=2.0)
            if i in [3,4]:
                p300_multi.move_to(plate_dils[s][Wells_dilution[i]].bottom(z=3))
                p300_multi.mix(3,150,plate_dils[s][Wells_dilution[i]].bottom(z=3),rate=2.0)
                p300_multi.aspirate(50,plate_dils[s][Wells_dilution[i]].bottom(z=3))
                p300_multi.dispense(50,plate_dils[s][Wells_dilution[i+1]].top(),rate=0.78)
                p300_multi.blow_out()
                p300_multi.mix(12,150,plate_dils[s][Wells_dilution[i+1]].bottom(z=3),rate=2.0)

            if i == 6:
                    p300_multi.drop_tip()
                    p300_multi.pick_up_tip()

            if i in [6,7,8]:
                    p300_multi.move_to(plate_dils[s][Wells_dilution[i]].bottom(z=3))
                    p300_multi.mix(3,150,plate_dils[s][Wells_dilution[i]].bottom(z=3),rate=2.0)
                    p300_multi.aspirate(20,plate_dils[s][Wells_dilution[i]].bottom(z=3))
                    p300_multi.dispense(20,plate_dils[s][Wells_dilution[i+1]].top(),rate=0.78)
                    p300_multi.blow_out()
                    p300_multi.mix(12,150,plate_dils[s][Wells_dilution[i+1]].bottom(z=3),rate=2.0)
            if i in [9,10]:
                    p300_multi.move_to(plate_dils[s][Wells_dilution[i]].bottom(z=3))
                    p300_multi.mix(3,150,plate_dils[s][Wells_dilution[i]].bottom(z=3),rate=2.0)
                    p300_multi.aspirate(50,plate_dils[s][Wells_dilution[i]].bottom(z=3))
                    p300_multi.dispense(50,plate_dils[s][Wells_dilution[i+1]].top(),rate=0.78)
                    p300_multi.blow_out()
                    p300_multi.mix(12,150,plate_dils[s][Wells_dilution[i+1]].bottom(z=3),rate=2.0)
        ctx.pause('remove the plate, then go to next plate')
        p300_multi.drop_tip()
