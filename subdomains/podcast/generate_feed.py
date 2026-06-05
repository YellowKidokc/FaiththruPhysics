import xml.etree.ElementTree as ET
from xml.dom import minidom
import datetime

rss = ET.Element('rss', {
    'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
    'xmlns:content': 'http://purl.org/rss/1.0/modules/content/',
    'version': '2.0'
})
channel = ET.SubElement(rss, 'channel')

ET.SubElement(channel, 'title').text = 'The Theophysics Podcast'
ET.SubElement(channel, 'link').text = 'https://podcast.faiththruphysics.com'
ET.SubElement(channel, 'language').text = 'en-us'
ET.SubElement(channel, 'description').text = (
    'The official podcast of the Theophysics Research Initiative. '
    'Ten episodes walking the full framework — from the coherence metric to the American collapse. '
    'Hosted by David Lowe.'
)
ET.SubElement(channel, 'lastBuildDate').text = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
ET.SubElement(channel, 'generator').text = 'Theophysics Podcast Generator'

ITUNES = 'http://www.itunes.com/dtds/podcast-1.0.dtd'
ET.SubElement(channel, '{%s}author' % ITUNES).text = 'David Lowe'
ET.SubElement(channel, '{%s}category' % ITUNES, {'text': 'Science'})
ET.SubElement(channel, '{%s}category' % ITUNES, {'text': 'Religion & Spirituality'})
ET.SubElement(channel, '{%s}explicit' % ITUNES).text = 'no'
ET.SubElement(channel, '{%s}image' % ITUNES, {'href': 'https://faiththruphysics.com/favicon.svg'})

image = ET.SubElement(channel, 'image')
ET.SubElement(image, 'url').text = 'https://faiththruphysics.com/favicon.svg'
ET.SubElement(image, 'title').text = 'The Theophysics Podcast'
ET.SubElement(image, 'link').text = 'https://podcast.faiththruphysics.com'

episodes = [
    {'num': 1, 'title': 'An Introduction to Theophysics', 'desc': 'What the framework is, why it exists, and how physics and theology speak the same language.', 'duration': '24:00', 'src': 'https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/podcast/01-an-introduction-to-theophysics.mp3'},
    {'num': 2, 'title': 'The Coherence Metric', 'desc': 'χ — the central state variable. How to measure the togetherness of anything from a laser to a marriage.', 'duration': '22:00', 'src': 'https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/podcast/02-the-coherence-metric.mp3'},
    {'num': 3, 'title': 'The Only Top-Down Framework', 'desc': 'Why every other unification attempt fails — and why Theophysics starts from information, not matter.', 'duration': '18:00', 'src': 'https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/podcast/03-the-only-top-down-framework.mp3'},
    {'num': 4, 'title': 'The American Coherence Collapse', 'desc': "Measuring the χ-field across 125 years of American history. The data is worse than you think.", 'duration': '26:00', 'src': 'https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/podcast/04-the-american-coherence-collapse.mp3'},
    {'num': 5, 'title': 'Fruits of the Spirit', 'desc': 'Galatians 5:22–23 as a compression block. Love, joy, peace — each fruit maps to a physical invariant.', 'duration': '32:00', 'src': 'https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/podcast/05-fruits-of-the-spirit.mp3'},
    {'num': 6, 'title': 'The Scientific Method Redux', 'desc': 'The 7-Question Scientific Method — a universal classifier that collapses all inquiry into one engine.', 'duration': '14:00', 'src': 'https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/podcast/06-the-scientific-method-redux.mp3'},
    {'num': 7, 'title': 'Master Coherence Analysis', 'desc': 'Walking the full Master Equation factor by factor. Ten variables, one coherence output.', 'duration': '19:00', 'src': 'https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/podcast/07-master-coherence-analysis.mp3'},
    {'num': 8, 'title': 'The Thermodynamics of Grace', 'desc': 'Grace as negentropy input. Why the Second Law forbids self-salvation — and why grace must come from outside.', 'duration': '16:00', 'src': 'https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/podcast/08-the-thermodynamics-of-grace.mp3'},
    {'num': 9, 'title': 'Church Debris Audit', 'desc': 'What survived the American church collapse — and what did not. A forensic analysis of institutional coherence loss.', 'duration': '28:00', 'src': 'https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/podcast/09-church-debris-audit.mp3'},
    {'num': 10, 'title': 'Cliodynamic Analysis — The Great Demoralization', 'desc': "Using Peter Turchin's cliodynamics to predict the 2020s crisis — and measuring it with the χ-field.", 'duration': '25:00', 'src': 'https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/podcast/10-cliodynamic-analysis-great-demoralization.mp3'},
]

for ep in episodes:
    item = ET.SubElement(channel, 'item')
    ET.SubElement(item, 'title').text = f"Ep {ep['num']:02d}: {ep['title']}"
    ET.SubElement(item, 'link').text = f"https://podcast.faiththruphysics.com/#ep{ep['num']}"
    ET.SubElement(item, 'guid', {'isPermaLink': 'false'}).text = f"theophysics-podcast-ep{ep['num']:02d}"
    pub = datetime.datetime(2026, 4, 26) + datetime.timedelta(days=ep['num'])
    ET.SubElement(item, 'pubDate').text = pub.strftime('%a, %d %b %Y %H:%M:%S +0000')
    ET.SubElement(item, 'description').text = ep['desc']
    ET.SubElement(item, 'enclosure', {'url': ep['src'], 'type': 'audio/mpeg', 'length': '0'})
    ET.SubElement(item, '{%s}duration' % ITUNES).text = ep['duration']
    ET.SubElement(item, '{%s}episode' % ITUNES).text = str(ep['num'])
    ET.SubElement(item, '{%s}explicit' % ITUNES).text = 'no'

xml_str = ET.tostring(rss, encoding='unicode')
dom = minidom.parseString(xml_str)
pretty = dom.toprettyxml(indent='  ')
lines = [line for line in pretty.split('\n') if line.strip()]
output = '\n'.join(lines)

with open(r'\\dlowenas\HPWorkstation\Desktop\Master HTMl\K-Production-Ready\subdomains\podcast\feed.xml', 'w', encoding='utf-8') as f:
    f.write(output)
print('RSS feed generated: feed.xml')
