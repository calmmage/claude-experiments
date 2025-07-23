# Todo

## Better cool ideas for projects (ALL enabled by default)

- [ ] Implement enum mode = ALL: randomly pick which idea generation mode to use
- [ ] Plain list of ideas
- [ ] Structured brainstorm, inspired areas like tech frameworks or other
- [ ] Generate idea with AI
- [ ] Structured AI generation - first, generate a direction, then pick a random one, then use direction to generate an idea

## Better project implementation scenario (staged development)

- [ ] Implement staged development with commits after each stage:
  - [ ] Stage 1: Simplest tech test + commit
  - [ ] Stage 2: MVP of meaningful core feature + commit
  - [ ] Stage 3: Complete functional scenario with UI + commit
- [ ] Add intermediary brainstorming/ideation between stages
- [ ] Save all intermediary results to work session
- [ ] Add evaluation system: Claude rates each stage 0-10 for:
  - [ ] Correspondence to original criteria
  - [ ] Current launchability/completeness
  - [ ] Save evaluation scores to work session metadata
- [ ] Implement safeguards:
  - [ ] Stop development after too many retries
  - [ ] Time limit per session (up to 12h is acceptable)
  - [ ] Quota management for Claude calls

## Idea and work session tracking

- [ ] Implement basic idea and work session tracking (MongoDB or disk storage)
- [ ] Ideas collection - add ideas when they are selected for implementation
- [ ] Work session collection - track when and where we worked on each idea
  - [ ] Support multiple work sessions per idea (follow-up features, retries)
  - [ ] Track if same place (follow-up) or new place (retry)
  - [ ] Record session metadata: timestamp, location, implementation level, success/failure
- [ ] Future: Simple CLI to manually add ideas to the ideas collection