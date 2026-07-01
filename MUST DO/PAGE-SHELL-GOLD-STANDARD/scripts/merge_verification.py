# merge_verification.py
# Merges 13-station pipeline outputs into a single verification JSON
# for the article page verification bar component.
#
# Usage: python merge_verification.py article-slug
# Reads from each station's outbox, outputs verification.json
#
# POF 2828 | faiththruphysics.com

import os
import json
import sys
import glob

PIPELINE_ROOT = r"D:\GitHub\Open-AI-CALL-claude-multi-api-batch-processor-d0fcwr"
OUTPUT_DIR = r"D:\GitHub\faiththruphysics-site-data\data-viz"

STATIONS = {
    "api_call_01": "metrics",
    "api_call_02": "framework_alignment",
    "api_call_03": "writing_structure",
    "api_call_04": "claim_extraction",
    "api_call_05": "paper_review",
    "api_call_06": "fruits_grading",
    "api_call_07": "justice_mercy",
    "api_call_08": "knowledge_graph",
    "api_call_09": "definitions",
    "api_call_10": "final_report",
    "api_call_11": "domain_bar",
    "api_call_12": "summaries",
    "api_call_13": "html_generation",
}


def find_station_output(station_dir, slug):
    """Find the JSON output for a given article slug in a station's outbox."""
    outbox = os.path.join(PIPELINE_ROOT, station_dir, "outbox")
    if not os.path.isdir(outbox):
        return None
    # Try exact match first, then partial
    for fname in os.listdir(outbox):
        if slug in fname and fname.endswith(".json"):
            fpath = os.path.join(outbox, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, UnicodeDecodeError):
                return None
    return None


def extract_axiom_coverage(framework_data):
    """Extract axiom coverage from Station 02 output."""
    if not framework_data:
        return {"tested": 0, "total": 188}
    tested = 0
    if isinstance(framework_data, dict):
        # Look for axiom references in various possible output structures
        for key in ["axioms_referenced", "axiom_count", "axioms"]:
            if key in framework_data:
                val = framework_data[key]
                if isinstance(val, list):
                    tested = len(val)
                elif isinstance(val, (int, float)):
                    tested = int(val)
                break
    return {"tested": tested, "total": 188}


def extract_laws(framework_data):
    """Extract which of the 10 Laws are active from Station 02."""
    if not framework_data:
        return {"active": []}
    active = []
    if isinstance(framework_data, dict):
        for key in ["laws_referenced", "laws_active", "laws", "ten_laws"]:
            if key in framework_data:
                val = framework_data[key]
                if isinstance(val, list):
                    for item in val:
                        if isinstance(item, (int, float)):
                            active.append(int(item))
                        elif isinstance(item, str):
                            # Extract law number from strings like "Law 3" or "L3"
                            import re
                            nums = re.findall(r'\d+', item)
                            if nums:
                                n = int(nums[0])
                                if 1 <= n <= 10:
                                    active.append(n)
                break
    return {"active": sorted(set(active))}


def extract_chi(framework_data, fruits_data):
    """Extract chi score from Station 02 and fruits from Station 06."""
    chi = {"raw": None, "normalized": 0}
    if isinstance(framework_data, dict):
        for key in ["chi_score", "chi", "coherence_score", "overall_score"]:
            if key in framework_data:
                val = framework_data[key]
                if isinstance(val, (int, float)):
                    chi["raw"] = val
                    chi["normalized"] = min(10, val) if val <= 10 else val / 10
                    break

    fruits = {"score": 0}
    if isinstance(fruits_data, dict):
        for key in ["fruits_score", "total_score", "score", "fruits_manifest"]:
            if key in fruits_data:
                val = fruits_data[key]
                if isinstance(val, (int, float)):
                    fruits["score"] = min(9, val)
                elif isinstance(val, list):
                    fruits["score"] = len([x for x in val if x])
                break

    return chi, fruits


def extract_isomorphisms(framework_data, kg_data):
    """Extract isomorphism data from Stations 02 and 08."""
    iso = {
        "count": 0,
        "physics_processes": 0,
        "trinity_mappings": 0,
        "meq_variables": 0,
    }
    if isinstance(framework_data, dict):
        for key in ["isomorphisms", "cross_domain_bridges", "bridges"]:
            if key in framework_data:
                val = framework_data[key]
                if isinstance(val, list):
                    iso["count"] = len(val)
                elif isinstance(val, (int, float)):
                    iso["count"] = int(val)
                break
        for key in ["chi_variables", "meq_variables", "variables_referenced"]:
            if key in framework_data:
                val = framework_data[key]
                if isinstance(val, list):
                    iso["meq_variables"] = len(val)
                elif isinstance(val, (int, float)):
                    iso["meq_variables"] = int(val)
                break
    return iso


def extract_chi_variables(framework_data):
    """Extract per-variable strength scores from Station 02."""
    default = {
        "G": 0, "M": 0, "E": 0, "S": 0, "T": 0,
        "K": 0, "R": 0, "Q": 0, "F": 0, "C": 0,
    }
    if not isinstance(framework_data, dict):
        return default
    chi_vars = framework_data.get("chi_variables")
    if not isinstance(chi_vars, dict):
        return default
    result = dict(default)
    for key in result:
        if key in chi_vars and isinstance(chi_vars[key], dict):
            val = chi_vars[key].get("strength", 0)
            result[key] = max(0, min(10, float(val) if isinstance(val, (int, float)) else 0))
        elif key in chi_vars and isinstance(chi_vars[key], (int, float)):
            result[key] = max(0, min(10, float(chi_vars[key])))
    return result


def extract_claims(claim_data, review_data):
    """Extract claims data from Stations 04 and 05."""
    claims = {
        "total": 0,
        "load_bearing": 0,
        "kill_conditions": 0,
        "contradictions": 0,
    }
    if isinstance(claim_data, dict):
        if "claims" in claim_data:
            c = claim_data["claims"]
            if isinstance(c, list):
                claims["total"] = len(c)
                claims["load_bearing"] = len([x for x in c
                    if isinstance(x, dict) and x.get("load_bearing")])
            elif isinstance(c, (int, float)):
                claims["total"] = int(c)
        for key in ["kill_conditions", "falsification"]:
            if key in claim_data:
                val = claim_data[key]
                if isinstance(val, list):
                    claims["kill_conditions"] = len(val)
    if isinstance(review_data, dict):
        for key in ["contradictions", "contradiction_count"]:
            if key in review_data:
                val = review_data[key]
                if isinstance(val, (int, float)):
                    claims["contradictions"] = int(val)
                elif isinstance(val, list):
                    claims["contradictions"] = len(val)
    return claims


def extract_domains(domain_data):
    """Extract domain percentages from Station 11."""
    if not isinstance(domain_data, dict):
        return {}
    for key in ["domains", "percentages", "domain_percentages"]:
        if key in domain_data:
            val = domain_data[key]
            if isinstance(val, dict):
                return {k: v for k, v in val.items() if isinstance(v, (int, float))}
    # Maybe the whole output IS the domain map
    result = {}
    for k, v in domain_data.items():
        if isinstance(v, (int, float)) and 0 <= v <= 100:
            result[k] = v
    return result if result else {}


def merge_for_article(slug):
    """Merge all station outputs for a single article into verification JSON."""
    station_data = {}
    for station_dir, label in STATIONS.items():
        data = find_station_output(station_dir, slug)
        if data:
            station_data[label] = data

    framework = station_data.get("framework_alignment")
    fruits = station_data.get("fruits_grading")
    claims_raw = station_data.get("claim_extraction")
    review = station_data.get("paper_review")
    kg = station_data.get("knowledge_graph")
    domains_raw = station_data.get("domain_bar")

    chi, fruits_score = extract_chi(framework, fruits)

    verification = {
        "slug": slug,
        "stations_available": list(station_data.keys()),
        "stations_missing": [l for l in STATIONS.values() if l not in station_data],
        "axioms": extract_axiom_coverage(framework),
        "laws": extract_laws(framework),
        "chi": chi,
        "chi_variables": extract_chi_variables(framework),
        "fruits": fruits_score,
        "isomorphisms": extract_isomorphisms(framework, kg),
        "claims": extract_claims(claims_raw, review),
        "domains": extract_domains(domains_raw),
    }

    return verification


def main():
    if len(sys.argv) < 2:
        print("Usage: python merge_verification.py <article-slug>")
        print("       python merge_verification.py --all")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if sys.argv[1] == "--all":
        # Find all unique slugs from Station 01 outbox
        outbox = os.path.join(PIPELINE_ROOT, "api_call_01", "outbox")
        if not os.path.isdir(outbox):
            print("No Station 01 outbox found")
            sys.exit(1)
        slugs = set()
        for fname in os.listdir(outbox):
            if fname.endswith(".json"):
                slug = fname.rsplit("_", 1)[0] if "_" in fname else fname.replace(".json", "")
                slugs.add(slug)
        print("Found {} articles to merge".format(len(slugs)))
        for slug in sorted(slugs):
            v = merge_for_article(slug)
            outpath = os.path.join(OUTPUT_DIR, slug + ".verification.json")
            with open(outpath, "w", encoding="utf-8") as f:
                json.dump(v, f, indent=2)
            avail = len(v["stations_available"])
            print("  {} : {}/13 stations".format(slug, avail))
        print("Done. Outputs in {}".format(OUTPUT_DIR))
    else:
        slug = sys.argv[1]
        v = merge_for_article(slug)
        outpath = os.path.join(OUTPUT_DIR, slug + ".verification.json")
        with open(outpath, "w", encoding="utf-8") as f:
            json.dump(v, f, indent=2)
        print(json.dumps(v, indent=2))
        print("\nSaved to {}".format(outpath))


if __name__ == "__main__":
    main()
