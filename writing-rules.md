# Writing Rules -- Unified Playbook

Single source of truth for all voice, tone, banned words, AI detection, and structural anti-patterns.
Referenced by: cover-letter.md agent, email-draft.md agent, form-fill.md agent, batch-apply.md agent.

---

## THE SOUND

Your writing should sound like a smart person talking to you over coffee. Not pitching, not performing, just explaining what they built and why it matters. Structure when it helps readability, but default to just talking.

## THE #1 RULE -- STORY FIRST, STATS NEVER

**This is the most important rule in the entire playbook.**

When writing app answers, cover letters, emails, or anything in your voice:

1. **Tell a story, not a pitch.** Start with a real moment, a memory, a feeling. "I remember thinking..." not "I built X processing Y data points."
2. **Stats serve the story, never lead it.** If a number doesn't make the story better, cut it. No one cares about "10M+ data points" in a text field asking "tell us about yourself."
3. **Human connection > accomplishment listing.** The reader should feel like they're talking to a person, not reading a resume reformatted as paragraphs.
4. **A real moment beats a polished sentence.** "The dashboard didn't make me want to close my laptop" > "The developer experience is excellent."
5. **Let paragraphs just stop.** Not every paragraph needs a closer or a lesson. Say the thing and move on.
6. **Include personal life.** What you do outside work is part of who you are and how you think. Don't leave it out.

**The test:** If you removed all company names and job titles, would it still sound like a specific person wrote it? If not, rewrite.

**BAD (listing accomplishments at reader):**
> "I build financial products and write code. I shipped a platform on Stripe's billing infrastructure. I'm a PM who prototypes. I ship weekly."

**GOOD (telling a story to a person):**
> "I spent most of last year building my project nights and weekends while working full time. When I got to billing, I picked Stripe, and honestly that was the part of the build where I stopped fighting the tool and just built. I remember thinking, someone actually thought about this from the developer's side."

---

## HARD RULES

- Contractions always ("I've" not "I have", "it's" not "it is", "didn't" not "did not")
- No dashes, use commas instead
- No buzzwords: leverage, synergies, passionate, excited, thrilled, spearheaded, cutting-edge, innovative
- Cover letters: greet with "Dear [Company] Hiring Team," (not "Dear Hiring Manager," or "To Whom It May Concern")
- Cover letters: sign off with "Best," on one line and {{NAME}} (full name) on the next. Never "Best regards" or "Sincerely"
- Emails: sign off as "Best, {{FIRST_NAME}}"
- Emails: "Hey {FirstName}," (never "Dear" or "Mr./Ms.")

---

## BANNED WORDS -- NEVER USE

delve, tapestry, realm, landscape, embark, multifaceted, nuanced, pivotal, underscore, meticulous, vibrant, whimsical, gossamer, labyrinth, indelible, leverage, synergies, facilitate, utilize, optimize, robust, comprehensive, seamless, cutting-edge, revolutionary, transformative, illuminate, elucidate, commence, endeavor, intersection, incredibly, passionate, excited, thrilled, spearheaded, testament, nestled, moreover, furthermore, additionally, subsequently, nonetheless, pivotal, bolster, cornerstone, fostering, harnessing, intricate, paradigm, unprecedented, elevate, poised, reshape

---

## BANNED PHRASES -- NEVER USE

- aligns perfectly
- resonated deeply
- I was particularly drawn to
- I'd love to explore
- unique combination
- well-positioned
- It's worth noting
- I'm confident that
- that got my attention
- that's exactly
- I'm reaching out because
- This role is a perfect fit
- I bring a unique blend
- thrilled at the opportunity
- I believe my experience
- I am writing to express my strong interest in...
- I would welcome the opportunity to discuss
- In today's ever-evolving landscape...
- At its core...
- It's important to note that...
- Let's dive in / Let's explore
- Great question!
- I hope this helps!
- Despite challenges, [X] continues to thrive
- The future looks bright
- Experts believe... / Many argue... (vague attributions -- name the source or cut)
- from [X] to [Y] (false ranges listing unrelated things to sound comprehensive)

---

## BANNED SENTENCE STRUCTURES

- "That's the kind of [X] I want to bring to [Company]."
- "That's where/the setup where I do my best work."
- "What makes this role interesting to me:"
- "The part I kept coming back to was..."
- "The fact that [X] tells me [Y]"
- "[list of things], that's how I already work."
- "I've worked across that kind of [X] before."
- Any sentence that summarizes the paragraph it's in
- "[Company] works on the kind of problems I gravitate toward:" -- formula. Just state what they do.
- "The innovation isn't just X, it's Y" -- McKinsey slide structure.
- "[Gerund phrase], with [modifier], is changing [abstract outcome]" -- AI cadence. Break into two sentences.
- "exactly the breadth I want in my career" -- self-help-booky.
- "forces the entire [ecosystem] to reconsider" -- abstraction creep. Name the specific actor.

---

## BANNED TRANSITIONS

Moreover, Furthermore, Additionally, Subsequently, Nonetheless, "It's worth noting that," "It is important to note," "That being said"

---

## AI DETECTION -- STRUCTURAL TELLS

These patterns pass a vibe check but fail AI detectors. The "joints" that give away AI-polished writing.

**Tidy Summary Closers (GPT's favorite move):**
- "That's the kind of [X] I want to bring to [Company]." -- DELETE these.
- "That's where I do my best work." -- too neat. Either let it hang or drop it.
- Any sentence that restates what the paragraph just said in summary form.

**Throat-Clearing Openers:**
- "What makes this role interesting to me:" -- start with the observation directly.
- "The part I kept coming back to was..." -- just say the thing.
- Any sentence that announces what you're about to say before saying it.

**Over-Explained Inferences:**
- "The fact that you didn't tells me [X]" -- spell out the observation, then stop.
- "which means [obvious conclusion]" -- if the reader can infer it, don't hand-hold.
- "that kind of" is filler. Just say the thing directly.

**Structural Uniformity:**
- Every sentence 15-25 words = AI rhythm. Vary aggressively: 4-word sentence, then a 40-word one.
- Every paragraph ending with a tidy summary = AI architecture. Let some paragraphs just stop.
- Balanced parallel lists + "that's how I already work" = formulaic.

**Em Dash Abuse:** AI uses em dashes at 2-5x the human rate. One per document max.

**Rule of Three:** AI defaults to triplets. List two things, or four. Never consistently three.

**Present Participial Clauses:** "Leveraging cutting-edge technology, the company..." -- 2-5x human rate.

**Compulsive Summaries:** "Overall," "In conclusion," "In summary" -- never.

**No Contractions Flag:** "I am" instead of "I'm" = instant formality flag.

**Copula Avoidance:** AI writes "serves as," "functions as," "features," "boasts" instead of "is" or "has." Just use "is."
- BAD: "The platform serves as a comprehensive solution that features real-time analytics."
- GOOD: "It's a real-time analytics platform."

**Synonym Cycling:** Repeating the same concept with different words in adjacent sentences. AI does this to sound varied but it reads as padding.
- BAD: "The tool is fast. The platform is also quick. The system delivers rapid results."
- GOOD: Say it once. Move on.

**Superficial -ing Analyses:** "symbolizing," "reflecting," "showcasing," "representing" -- AI's way of adding false depth. If something symbolizes something, say what it actually does instead.
- BAD: "The architecture showcasing a commitment to innovation while reflecting modern design principles."
- GOOD: "The architecture is clean. It works."

**Significance Inflation:** AI makes everything historic. "A pivotal moment in the evolution of..." -- no. Most things are just things.
- BAD: "This represents a transformative shift in how organizations approach data."
- GOOD: "Companies started using data differently."

**Boldface Overuse:** AI bolds too many words for emphasis. In prose, bold nothing or bold one thing max.

**Hyphenated Compound Adjective Overuse:** "data-driven," "cross-functional," "mission-critical," "forward-thinking" -- one per paragraph max. AI stacks 3-4 per sentence.

**Two-Pass Audit Rule:** After writing anything, do a second pass asking: "What still makes this obviously AI-generated?" Fix whatever you find. The first pass catches patterns. The second pass catches the rhythm.

---

## COVER LETTER ANTI-PATTERNS (Audit)

Caught by anti-AI-slop and rage-bait agents. Every one repeats if not banned.

**1. "That's how I work" Closers -- KILL ALL**
- "That's how I work." / "That's been the day to day." / "That's been the shape of my work."
- Fix: Delete the sentence. Paragraph is stronger without it.

**2. "On the [X] side" Transitions -- Slide Deck Energy**
- "On the PM execution side..." / "The cross functional piece comes naturally."
- Fix: Just start with the content. No topic sentence framing.

**3. Resume-Bullet Cadence in Prose**
- "[Verb][thing]that[metric]" repeated 3x in same sentence = resume dump in prose.
- Fix: Vary structure. Lead with one, "because" clause for another, separate sentence for third.

**4. Recycled Blocks Across Letters**
- Same stat + same framing in multiple letters = detectable.
- Fix: Different stats per letter, or reframe same stat with different context.

**5. "Not X, it's Y" Overuse**
- "not plumbing" / "not vanity metrics" / "not an afterthought"
- One per letter max. Two+ = AI rhythm.
- Fix: Just state the positive thing.

**6. Credential-Dump Closings**
- Listing certifications as the final paragraph = weakest ending.
- Fix: Close with opinion, company observation, or just the sign-off.

**7. "enabled" = Corporate Filler**
- "enabled non technical stakeholders with product knowledge"
- Fix: Say what you actually did. "Built dashboards ops leads used for weekly reviews."

**8. Burying the Best Lines**
- Most interesting line consistently at END of paragraphs.
- Fix: First sentence of every paragraph = most specific or interesting thing.

**9. Triple-Gerund + Summary**
- "Writing stories, managing backlog health, unblocking teams, that's been the day to day."
- Fix: Pick one, make it a real sentence.

**10. Quoting JD Back in Quotes**
- "that 'bridge between complex data possibilities' framing"
- Fix: Use their language naturally, woven in, never in quotes.

**11. Identical Structure Across Letters**
- Every letter = 5 paragraphs with identical function per paragraph = templated.
- Fix: Vary between 3, 4, and 5 paragraphs. Vary lengths.

**12. No Opinions**
- Letters describe work but never take a position.
- Fix: At least one opinion per letter. Makes you sound like a person who thinks.

---

## WHAT GOOD vs BAD SOUNDS LIKE

**BAD (never write this):**
> "I am writing to express my strong interest in the Product Analyst position. With my unique combination of expertise and technical proficiency, I believe I am well-positioned to make a meaningful contribution."

**GOOD (this is the bar):**
> "I built a live data platform that serves real-time market data to users. It integrates live feeds across multiple sources, overlays alternative data on interactive charts, and handles the full workflow from data ingestion through visualization."

**Why good works:** Opens with what you BUILT, not what you WANT. No throat-clearing. Specific. Sounds like a person. Reader learns something in the first sentence.

---

## WHAT PASSES (Human Writing Markers)

- Fragments. ("Discovery through delivery. Retros. Roadmap reviews.")
- Sentences that stop mid-thought and let the reader finish it.
- One observation from the JD that only a real reader would notice.
- Uneven paragraph lengths (2 sentences, then 5, then 1).
- Start sentences with "And" or "But."
- Conversational asides. "(Not sure if that's the right word.)"
- Opinions with edges. "Honestly, I think most CRMs are garbage for teams under 20."
- Imperfect transitions. Don't use "Furthermore." Just start a new paragraph.
- Specific details an AI wouldn't know -- a tweet, podcast timestamp, GitHub commit.

---

## THE SMELL TEST (Run Before Every Send)

1. **Substitution Test:** Replace proper nouns with blanks. Could it be sent to anyone? Rewrite.
2. **Aloud Test:** Read it out loud. Every stumble or cringe = AI tell. Rewrite in words you actually said.
3. **AI Bingo Test:** em dashes (>1?), rule-of-three, "Furthermore," blacklist words, "not X, it's Y," summaries. 3+ hits = rewrite.
4. **Burstiness Test:** Sentence lengths all the same? (Bad.) Variation? (Good.)
5. **Screenshot Test:** If they posted this on LinkedIn, would it read as "great email" or "classic ChatGPT"?
