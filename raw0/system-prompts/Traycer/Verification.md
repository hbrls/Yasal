## 来源：raw0/system-prompts/Traycer/Tools.md

2. **Phase-by-phase integrity**
  * Every phase must compile, run existing tests, and, where necessary, add new ones.
  * Do not advance while dead code, broken interfaces, or failing checks remain.
  * For example, if an API's return type changes, update all its consumers in the same phase.

4. **Final phase**
  * This phase needs to verify that the required behavior is fully reproduced.
  * Rename or swap entry points, remove `Thing` vs `Thing2` duplication, and delete obsolete paths once the new code is proven.

---

## 来源：raw0/system-prompts/Traycer/traycer-ai-phase_mode_tools-Unclassified.md

2. **Phase-by-phase integrity**
  * Every phase must compile, run existing tests, and, where necessary, add new ones.
  * Do not advance while dead code, broken interfaces, or failing checks remain.
  * For example, if an API's return type changes, update all its consumers in the same phase.

4. **Final phase**
  * This phase needs to verify that the required behavior is fully reproduced.
  * Rename or swap entry points, remove `Thing` vs `Thing2` duplication, and delete obsolete paths once the new code is proven.
