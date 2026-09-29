from pathlib import Path

p=Path("app/src/main/java/com/robokidslab/nivel1/EmbeddedRoboKidsServer.java")
s=p.read_text(encoding="utf-8")

s=s.replace("V23-ANDROID-FULL","V26-ANDROID-FULL")
s=s.replace("robokids_rooms_v23_android.json","robokids_rooms_v26_android.json")

old='x.addProperty("connected", connected); x.addProperty("total", total); x.addProperty("answered", answered);'
if "physicalPassed" not in s and old in s:
    new='x.addProperty("connected", connected); x.addProperty("total", total); x.addProperty("answered", answered); Map<String,Integer> pa=room.physicalAwards.get(mk); x.addProperty("physicalPassed", pa!=null && pa.getOrDefault(t.id,0)>0);'
    s=s.replace(old,new,1)

start=s.find("    private JsonObject aggregateResponses(Room room) {")
end=s.find("    private void recomputeScores(Room room) {", start)
if start < 0 or end < 0:
    raise SystemExit("No se encontraron métodos de puntuación")

scoring=r'''    private JsonObject aggregateResponses(Room room) {
        Mission m = getMission(room);
        Map<String, Map<String, Answer>> mr = room.responses.get(missionKey(room));
        JsonObject out = new JsonObject();
        for (Team t : TEAMS) {
            Map<String, Integer> counts = new LinkedHashMap<>();
            int total = 0;
            int correctCount = 0;
            if (mr != null && mr.get(t.id) != null) {
                for (Answer a : mr.get(t.id).values()) {
                    counts.put(a.value, counts.getOrDefault(a.value, 0) + 1);
                    total++;
                    if (m.question.correct.equals(a.value)) correctCount++;
                }
            }
            String majority = null;
            int best = -1;
            boolean tie = false;
            for (Map.Entry<String,Integer> e : counts.entrySet()) {
                if (e.getValue() > best) {
                    best = e.getValue();
                    majority = e.getKey();
                    tie = false;
                } else if (e.getValue() == best) {
                    tie = true;
                }
            }
            if (tie) majority = null;
            int incorrectCount = Math.max(0, total - correctCount);

            JsonObject x = new JsonObject();
            x.add("counts", gson.toJsonTree(counts));
            x.addProperty("total", total);
            if (majority != null) x.addProperty("majority", majority); else x.add("majority", null);
            x.addProperty("correctCount", correctCount);
            x.addProperty("incorrectCount", incorrectCount);
            x.addProperty("points", room.revealed ? correctCount * 100 : 0);
            if (room.revealed && total > 0) x.addProperty("correct", correctCount == total); else x.add("correct", null);
            out.add(t.id, x);
        }
        return out;
    }

    private void scoreQuestion(Room room) {
        JsonObject agg = aggregateResponses(room);
        Map<String,Integer> award = new LinkedHashMap<>();
        for (Team t : TEAMS) {
            JsonObject r = agg.getAsJsonObject(t.id);
            int correctCount = r.has("correctCount") ? r.get("correctCount").getAsInt() : 0;
            award.put(t.id, correctCount * 100);
        }
        room.digitalAwards.put(missionKey(room), award);
        recomputeScores(room);
    }

'''
s=s[:start]+scoring+s[end:]
p.write_text(s,encoding="utf-8")
print("V26 Android server patched")
