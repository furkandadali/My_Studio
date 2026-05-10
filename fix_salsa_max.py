#!/usr/bin/env python3
"""Fix Avaturn SALSA components in Main.unity:
   1. maxShape: 0.01 → maxShape: 1 (Salsa3D visemes)
   2. Clean head bone ctrl in RandomEyes3D (remove wrong smr/blendIndex, strip 2 extra entries)
   3. Fix eye flags + rebuild eyes/blinklids sections
"""
import sys

PATH = '/Volumes/D/Prototypes/My_Studio/Assets/Scenes/Main.unity'

with open(PATH, 'r') as f:
    content = f.read()

# ── 1. maxShape: 0.01 → 1 ────────────────────────────────────────────────────
before = content.count('        maxShape: 0.01\n')
assert before > 0, "No maxShape: 0.01 found"
content = content.replace('        maxShape: 0.01\n', '        maxShape: 1\n')
print(f"[1] Fixed {before} maxShape: 0.01 → 1")

# ── 2. Fix head bone ctrl + remove 2 extra entries ───────────────────────────
old_head_tail = (
    '        smr: {fileID: 8063369713455366259}\n'
    '        blendIndex: 44\n'
    '        minShape: 0\n'
    '        maxShape: 1\n'
    '        eyeGizmo: {fileID: 0}\n'
    '        eventSender: {fileID: 0}\n'
    '        animator: {fileID: 0}\n'
    '        isTriggerParameterBiDirectional: 0\n'
    '        eventIdentityName: \n'
    '        onState: 2\n'
    '        display2dImage: 0\n'
    '        isRestNull: 0\n'
    '        spriteRenderer: {fileID: 0}\n'
    '        sprites: []\n'
    '        uguiRenderer: {fileID: 0}\n'
    '        textureRenderer: {fileID: 0}\n'
    '        materialIndex: 0\n'
    '        backupTextures: []\n'
    '        textures: []\n'
    '        materialRenderer: {fileID: 0}\n'
    '        materials: []\n'
    '      - bone: {fileID: 0}\n'
    '        baseTform:\n'
    '          pos: {x: 0, y: 0, z: 0}\n'
    '          rot: {x: 0, y: 0, z: 0, w: 0}\n'
    '          scale: {x: 0, y: 0, z: 0}\n'
    '        startTform:\n'
    '          pos: {x: 0, y: 0, z: 0}\n'
    '          rot: {x: 0, y: 0, z: 0, w: 0}\n'
    '          scale: {x: 0, y: 0, z: 0}\n'
    '        endTform:\n'
    '          pos: {x: 0, y: 0, z: 0}\n'
    '          rot: {x: 0, y: 0, z: 0, w: 0}\n'
    '          scale: {x: 0, y: 0, z: 0}\n'
    '        fracPos: 1\n'
    '        fracRot: 0\n'
    '        fracScl: 0\n'
    '        inspIsSetStart: 0\n'
    '        inspIsSetEnd: 0\n'
    '        umaUepProxy: {fileID: 0}\n'
    '        uepAmount: 0\n'
    '        smr: {fileID: 8063369713455366259}\n'
    '        blendIndex: 45\n'
    '        minShape: 0\n'
    '        maxShape: 1\n'
    '        eyeGizmo: {fileID: 0}\n'
    '        eventSender: {fileID: 0}\n'
    '        animator: {fileID: 0}\n'
    '        isTriggerParameterBiDirectional: 0\n'
    '        eventIdentityName: \n'
    '        onState: 2\n'
    '        display2dImage: 0\n'
    '        isRestNull: 0\n'
    '        spriteRenderer: {fileID: 0}\n'
    '        sprites: []\n'
    '        uguiRenderer: {fileID: 0}\n'
    '        textureRenderer: {fileID: 0}\n'
    '        materialIndex: 0\n'
    '        backupTextures: []\n'
    '        textures: []\n'
    '        materialRenderer: {fileID: 0}\n'
    '        materials: []\n'
    '      - bone: {fileID: 0}\n'
    '        baseTform:\n'
    '          pos: {x: 0, y: 0, z: 0}\n'
    '          rot: {x: 0, y: 0, z: 0, w: 0}\n'
    '          scale: {x: 0, y: 0, z: 0}\n'
    '        startTform:\n'
    '          pos: {x: 0, y: 0, z: 0}\n'
    '          rot: {x: 0, y: 0, z: 0, w: 0}\n'
    '          scale: {x: 0, y: 0, z: 0}\n'
    '        endTform:\n'
    '          pos: {x: 0, y: 0, z: 0}\n'
    '          rot: {x: 0, y: 0, z: 0, w: 0}\n'
    '          scale: {x: 0, y: 0, z: 0}\n'
    '        fracPos: 1\n'
    '        fracRot: 0\n'
    '        fracScl: 0\n'
    '        inspIsSetStart: 0\n'
    '        inspIsSetEnd: 0\n'
    '        umaUepProxy: {fileID: 0}\n'
    '        uepAmount: 0\n'
    '        smr: {fileID: 8063369713455366259}\n'
    '        blendIndex: 58\n'
    '        minShape: 0\n'
    '        maxShape: 1\n'
    '        eyeGizmo: {fileID: 0}\n'
    '        eventSender: {fileID: 0}\n'
    '        animator: {fileID: 0}\n'
    '        isTriggerParameterBiDirectional: 0\n'
    '        eventIdentityName: \n'
    '        onState: 2\n'
    '        display2dImage: 0\n'
    '        isRestNull: 0\n'
    '        spriteRenderer: {fileID: 0}\n'
    '        sprites: []\n'
    '        uguiRenderer: {fileID: 0}\n'
    '        textureRenderer: {fileID: 0}\n'
    '        materialIndex: 0\n'
    '        backupTextures: []\n'
    '        textures: []\n'
    '        materialRenderer: {fileID: 0}\n'
    '        materials: []\n'
)
new_head_tail = (
    '        smr: {fileID: 0}\n'
    '        blendIndex: 0\n'
    '        minShape: 0\n'
    '        maxShape: 1\n'
    '        eyeGizmo: {fileID: 0}\n'
    '        eventSender: {fileID: 0}\n'
    '        animator: {fileID: 0}\n'
    '        isTriggerParameterBiDirectional: 0\n'
    '        eventIdentityName: \n'
    '        onState: 2\n'
    '        display2dImage: 0\n'
    '        isRestNull: 0\n'
    '        spriteRenderer: {fileID: 0}\n'
    '        sprites: []\n'
    '        uguiRenderer: {fileID: 0}\n'
    '        textureRenderer: {fileID: 0}\n'
    '        materialIndex: 0\n'
    '        backupTextures: []\n'
    '        textures: []\n'
    '        materialRenderer: {fileID: 0}\n'
    '        materials: []\n'
)
assert old_head_tail in content, "Head ctrl tail pattern not found!"
content = content.replace(old_head_tail, new_head_tail, 1)
print("[2] Fixed head bone ctrl (cleared smr/blendIndex, removed 2 extra entries)")

# ── 3. Fix eye flags ──────────────────────────────────────────────────────────
assert content.count('  eyeTemplate: 0\n') == 1, "eyeTemplate not unique"
assert content.count('  useEyeShapes: 0\n') == 1, "useEyeShapes not unique"
assert content.count('  eyelidTemplate: 0\n') == 1, "eyelidTemplate not unique"
assert content.count('  eyelidSelection: 0\n') == 1, "eyelidSelection not unique"

content = content.replace('  eyeTemplate: 0\n',    '  eyeTemplate: 3\n')
content = content.replace('  useEyeShapes: 0\n',   '  useEyeShapes: 1\n')
content = content.replace('  eyelidTemplate: 0\n', '  eyelidTemplate: 3\n')
content = content.replace('  eyelidSelection: 0\n','  eyelidSelection: 1\n')
print("[3] Fixed eye flags (eyeTemplate→3, useEyeShapes→1, eyelidTemplate→3, eyelidSelection→1)")

# ── helpers ───────────────────────────────────────────────────────────────────
SMR = '8063369713455366259'

def ctrl_var(blend_idx):
    return (
        f'      - bone: {{fileID: 0}}\n'
        f'        baseTform:\n'
        f'          pos: {{x: 0, y: 0, z: 0}}\n'
        f'          rot: {{x: 0, y: 0, z: 0, w: 0}}\n'
        f'          scale: {{x: 0, y: 0, z: 0}}\n'
        f'        startTform:\n'
        f'          pos: {{x: 0, y: 0, z: 0}}\n'
        f'          rot: {{x: 0, y: 0, z: 0, w: 0}}\n'
        f'          scale: {{x: 0, y: 0, z: 0}}\n'
        f'        endTform:\n'
        f'          pos: {{x: 0, y: 0, z: 0}}\n'
        f'          rot: {{x: 0, y: 0, z: 0, w: 0}}\n'
        f'          scale: {{x: 0, y: 0, z: 0}}\n'
        f'        fracPos: 1\n'
        f'        fracRot: 1\n'
        f'        fracScl: 1\n'
        f'        inspIsSetStart: 0\n'
        f'        inspIsSetEnd: 0\n'
        f'        umaUepProxy: {{fileID: 0}}\n'
        f'        uepAmount: 0\n'
        f'        smr: {{fileID: {SMR}}}\n'
        f'        blendIndex: {blend_idx}\n'
        f'        minShape: 0\n'
        f'        maxShape: 1\n'
        f'        eyeGizmo: {{fileID: 0}}\n'
        f'        eventSender: {{fileID: 0}}\n'
        f'        animator: {{fileID: 0}}\n'
        f'        isTriggerParameterBiDirectional: 0\n'
        f'        eventIdentityName: \n'
        f'        onState: 2\n'
        f'        display2dImage: 0\n'
        f'        isRestNull: 0\n'
        f'        spriteRenderer: {{fileID: 0}}\n'
        f'        sprites: []\n'
        f'        uguiRenderer: {{fileID: 0}}\n'
        f'        textureRenderer: {{fileID: 0}}\n'
        f'        materialIndex: 0\n'
        f'        backupTextures: []\n'
        f'        textures: []\n'
        f'        materialRenderer: {{fileID: 0}}\n'
        f'        materials: []'
    )

def eye_comp(name, direction_type, persistent=1):
    return (
        f'      - name: {name}\n'
        f'        controlType: 0\n'
        f'        lipsyncControlType: 0\n'
        f'        emoteControlType: 0\n'
        f'        eyesControlType: 1\n'
        f'        durationDelay: 0\n'
        f'        durationOn: 0.2\n'
        f'        durationHold: 0\n'
        f'        durationOff: 0.2\n'
        f'        isSmoothDisable: 0\n'
        f'        isPersistent: {persistent}\n'
        f'        expressionType: 0\n'
        f'        easing: 4\n'
        f'        expressionHandler: 0\n'
        f'        isAnimatorControlled: 0\n'
        f'        useOffset: 0\n'
        f'        useOffsetFollow: 1\n'
        f'        inspFoldout: 1\n'
        f'        enabled: 1\n'
        f'        isBonePreviewUpdated: 0\n'
        f'        frac: 1\n'
        f'        directionType: {direction_type}'
    )

def blink_comp(name):
    return (
        f'      - name: {name}\n'
        f'        controlType: 0\n'
        f'        lipsyncControlType: 0\n'
        f'        emoteControlType: 0\n'
        f'        eyesControlType: 1\n'
        f'        durationDelay: 0\n'
        f'        durationOn: 0.075\n'
        f'        durationHold: 0.05\n'
        f'        durationOff: 0.075\n'
        f'        isSmoothDisable: 0\n'
        f'        isPersistent: 0\n'
        f'        expressionType: 0\n'
        f'        easing: 4\n'
        f'        expressionHandler: 0\n'
        f'        isAnimatorControlled: 0\n'
        f'        useOffset: 0\n'
        f'        useOffsetFollow: 1\n'
        f'        inspFoldout: 1\n'
        f'        enabled: 1\n'
        f'        isBonePreviewUpdated: 0\n'
        f'        frac: 1\n'
        f'        directionType: 0'
    )

# ── 4. Rebuild eyes section ───────────────────────────────────────────────────
# directionType: 2=up, 6=down, 8=left(char), 4=right(char)
eye_shapes = [
    ('eyeLookUpLeft',    2, 52),
    ('eyeLookUpRight',   2, 53),
    ('eyeLookDownLeft',  6, 50),
    ('eyeLookDownRight', 6, 51),
    ('eyeLookOutLeft',   8, 56),
    ('eyeLookInRight',   8, 55),
    ('eyeLookInLeft',    4, 54),
    ('eyeLookOutRight',  4, 57),
]

eyes_comps = '\n'.join(eye_comp(n, dt) for n, dt, _ in eye_shapes)
eyes_cvars = '\n'.join(ctrl_var(bi)    for _, _, bi  in eye_shapes)

eyes_section = (
    '  eyes:\n'
    '  - expData:\n'
    '      name: eyes\n'
    '      components:\n'
    + eyes_comps + '\n'
    '      controllerVars:\n'
    + eyes_cvars + '\n'
    '      inspFoldout: 1\n'
    '      previewDisplayMode: 0\n'
    '      collectionExpand: 0\n'
    '    gizmo: {fileID: 0}\n'
    '    referenceIdx: 0'
)

assert '  eyes: []\n' in content, "eyes: [] not found"
content = content.replace('  eyes: []\n', eyes_section + '\n')
print("[4] Rebuilt eyes section with 8 ARKit eye-look blend shapes")

# ── 5. Rebuild blinklids section ──────────────────────────────────────────────
blink_shapes = [
    ('eyeBlinkLeft',  44),
    ('eyeBlinkRight', 45),
    ('eyesClosed',    58),
]

blink_comps = '\n'.join(blink_comp(n)  for n, _  in blink_shapes)
blink_cvars = '\n'.join(ctrl_var(bi)   for _, bi in blink_shapes)

blinklids_section = (
    '  blinklids:\n'
    '  - expData:\n'
    '      name: blink\n'
    '      components:\n'
    + blink_comps + '\n'
    '      controllerVars:\n'
    + blink_cvars + '\n'
    '      inspFoldout: 1\n'
    '      previewDisplayMode: 0\n'
    '      collectionExpand: 0\n'
    '    gizmo: {fileID: 0}\n'
    '    referenceIdx: 0'
)

assert '  blinklids: []\n' in content, "blinklids: [] not found"
content = content.replace('  blinklids: []\n', blinklids_section + '\n')
print("[5] Rebuilt blinklids section with eyeBlinkLeft/Right + eyesClosed")

# ── write ─────────────────────────────────────────────────────────────────────
with open(PATH, 'w') as f:
    f.write(content)

print("\nAll done. Main.unity updated.")
