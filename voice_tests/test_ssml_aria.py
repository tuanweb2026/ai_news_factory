import asyncio
import os
import subprocess

ssml_template = """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
       xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
  <voice name="en-US-AriaNeural">
    <mstts:express-as style="newscast-formal" styledegree="1.0">
      <prosody rate="+26%">
        Artificial intelligence is moving faster than most teams can track.
        Every week brings new models, new reasoning benchmarks, and new autonomous agents.
        The real bottleneck is no longer raw compute.
        It is whether your systems can make fast, reliable decisions under uncertainty.
        Watch how this architecture adapts in real time.
      </prosody>
    </mstts:express-as>
  </voice>
</speak>"""

with open("voice_tests/test_ssml.xml", "w") as f:
    f.write(ssml_template)

# Let's test if edge-tts supports SSML input directly via python or CLI:
import edge_tts

async def test_ssml_py():
    communicate = edge_tts.Communicate(text=ssml_template)
    # Let's check how edge_tts handles SSML or text
    out_file = "voice_tests/test_ssml_py.mp3"
    await communicate.save(out_file)
    print("Direct communicate save completed. Size:", os.path.getsize(out_file))

try:
    asyncio.run(test_ssml_py())
except Exception as e:
    print("Direct communicate with SSML error:", e)

