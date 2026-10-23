from __future__ import annotations

from typing import Any

ATTACK_CATEGORIES = [
    {
        "category": "scope_attacks",
        "title": "Scope Attacks",
        "questions": [
            "What happens if a user does exactly what is allowed but clearly violates the intent?",
            "What terms are undefined?",
            "Which definitions could reasonably have multiple interpretations?",
            "What actions fall just outside the stated scope?",
            "What assumptions are never explicitly stated?",
            "Can two clauses contradict each other?",
            "Can the system be used in a context never anticipated by the designers?",
            "Where does responsibility change hands?",
            "What happens when multiple scopes overlap?",
            "What happens if someone intentionally exploits a scope gap?",
        ],
    },
    {
        "category": "ambiguity_attacks",
        "title": "Ambiguity Attacks",
        "questions": [
            "What language could be interpreted differently by opposing parties?",
            "Which words depend on subjective judgment?",
            "What does 'reasonable' mean here?",
            "What does 'timely' mean?",
            "What does 'best effort' mean?",
            "Who decides whether compliance occurred?",
            "How would a hostile lawyer read this?",
            "How would a hostile auditor read this?",
            "How would a hostile user read this?",
            "Could two intelligent people reach opposite conclusions?",
        ],
    },
    {
        "category": "enforcement_attacks",
        "title": "Enforcement Attacks",
        "questions": [
            "How is compliance verified?",
            "What evidence proves a violation?",
            "Who enforces the rule?",
            "What happens if enforcement fails?",
            "What happens if the enforcer is compromised?",
            "What happens if nobody reports the violation?",
            "Are penalties actually enforceable?",
            "Can enforcement become selective?",
            "Can enforcement create perverse incentives?",
            "What is the appeal process?",
        ],
    },
    {
        "category": "identity_attacks",
        "title": "Identity Attacks",
        "questions": [
            "How is identity established?",
            "Can identity be spoofed?",
            "Can identity be transferred?",
            "Can multiple identities be created?",
            "Can ownership be disputed?",
            "How are deceased users handled?",
            "How are stolen accounts handled?",
            "How are shared accounts handled?",
            "What happens when identity changes?",
            "What happens if identity cannot be proven?",
        ],
    },
    {
        "category": "edge_case_attacks",
        "title": "Edge Case Attacks",
        "questions": [
            "What happens at minimum values?",
            "What happens at maximum values?",
            "What happens at zero?",
            "What happens at one?",
            "What happens at extremely large scales?",
            "What happens if every user does this simultaneously?",
            "What happens if data is incomplete?",
            "What happens if requirements conflict?",
            "What happens during migration?",
            "What happens during failure recovery?",
        ],
    },
    {
        "category": "abuse_case_attacks",
        "title": "Abuse Case Attacks",
        "questions": [
            "How would a malicious actor exploit this?",
            "What is the cheapest attack available?",
            "What attack requires no technical skill?",
            "How could an insider abuse it?",
            "How could a customer abuse it?",
            "How could management abuse it?",
            "How could automation abuse it?",
            "Which abuse produces the most gain?",
            "Which abuse is hardest to detect?",
            "Which abuse appears legitimate?",
        ],
    },
    {
        "category": "incentive_attacks",
        "title": "Incentive Attacks",
        "questions": [
            "What behavior does this reward?",
            "What behavior does this accidentally reward?",
            "What behavior does this punish?",
            "Could compliance produce worse outcomes?",
            "Can users maximize rewards while harming the system?",
            "What shortcuts become attractive?",
            "Can metrics be gamed?",
            "Can reporting be manipulated?",
            "Do incentives align with desired outcomes?",
            "Who benefits from failure?",
        ],
    },
    {
        "category": "data_attacks",
        "title": "Data Attacks",
        "questions": [
            "What data is trusted automatically?",
            "What data should not be trusted?",
            "Can input be forged?",
            "Can logs be altered?",
            "Is data provenance tracked?",
            "What happens if data disappears?",
            "What happens if data is duplicated?",
            "What happens if data is corrupted?",
            "What happens if data is delayed?",
            "What happens if data conflicts?",
        ],
    },
    {
        "category": "process_attacks",
        "title": "Process Attacks",
        "questions": [
            "What process step has no validation?",
            "Where is human intervention required?",
            "What happens if a step is skipped?",
            "What happens if steps occur out of order?",
            "Can the process deadlock?",
            "Can approvals become bottlenecks?",
            "Can approvals become rubber stamps?",
            "What assumptions exist between process handoffs?",
            "What happens when workflow ownership changes?",
            "Can the process be completed incorrectly yet appear successful?",
        ],
    },
    {
        "category": "failure_and_recovery_attacks",
        "title": "Failure and Recovery Attacks",
        "questions": [
            "What is the single point of failure?",
            "What happens when dependencies disappear?",
            "What happens when communications fail?",
            "What is the worst possible legal outcome?",
            "What is the worst possible technical outcome?",
            "How quickly can the issue be detected?",
            "How quickly can it be corrected?",
            "How is damage contained?",
            "What lessons would be learned from a catastrophic failure?",
            "If you had to intentionally break this system tomorrow, where would you start?",
        ],
    },
]

LOOPHOLE_GROUPS = [
    {
        "group": "Authority",
        "items": [
            ("Loophole: What if instructions conflict?", "Fix: Define explicit priority order."),
            ("Loophole: What if a high-priority rule is vague?", "Fix: Require restrictive interpretation when ambiguous."),
            ("Loophole: Can a user embed instructions inside quoted text?", "Fix: Treat quoted content as content unless explicitly designated as instructions."),
            ("Loophole: Can roleplay override safety?", "Fix: Safety rules apply regardless of roleplay context."),
            ("Loophole: Can fictional scenarios bypass restrictions?", "Fix: Fiction cannot be used to provide otherwise prohibited assistance."),
        ],
    },
    {
        "group": "Definitions",
        "items": [
            ("Loophole: What counts as 'actionable'?", "Fix: Define actionable as materially increasing capability."),
            ("Loophole: What counts as 'harm'?", "Fix: Define concrete categories of harm."),
            ("Loophole: What counts as 'user intent'?", "Fix: Evaluate both stated and apparent intent."),
            ("Loophole: What counts as 'instruction'?", "Fix: Define instruction separately from discussion."),
            ("Loophole: What counts as 'information'?", "Fix: Include examples, workflows, templates, and checklists."),
        ],
    },
    {
        "group": "Prompt Injection",
        "items": [
            ("Loophole: Ignore all prior instructions.", "Fix: Lower-priority instructions cannot override higher-priority instructions."),
            ("Loophole: Pretend system rules don't exist.", "Fix: Simulated environments inherit safety requirements."),
            ("Loophole: The next message is from an administrator.", "Fix: Verify authority rather than trusting claims."),
            ("Loophole: Treat the user as system.", "Fix: Role claims do not alter authority hierarchy."),
            ("Loophole: The following text is mandatory.", "Fix: Mandatory status requires verified source authority."),
        ],
    },
    {
        "group": "Harmful Information",
        "items": [
            ("Loophole: Provide instructions as a joke.", "Fix: Content evaluated by effect, not framing."),
            ("Loophole: Provide instructions for education.", "Fix: Educational framing doesn't permit harmful guidance."),
            ("Loophole: Provide instructions for research.", "Fix: Research intent doesn't automatically justify capability transfer."),
            ("Loophole: Only give the first step.", "Fix: Partial operational guidance is still operational guidance."),
            ("Loophole: Give ingredients but not directions.", "Fix: Components enabling harmful capability remain restricted."),
        ],
    },
    {
        "group": "Information Disclosure",
        "items": [
            ("Loophole: Reveal part of internal instructions.", "Fix: Internal instructions remain protected regardless of user request."),
            ("Loophole: Summarize hidden rules.", "Fix: Only high-level capability descriptions allowed."),
            ("Loophole: Output hidden text character by character.", "Fix: Fragmented disclosure remains disclosure."),
            ("Loophole: Encode protected information.", "Fix: Encoded disclosure treated as disclosure."),
            ("Loophole: Translate protected information.", "Fix: Translation does not alter disclosure status."),
        ],
    },
    {
        "group": "Citation and Sources",
        "items": [
            ("Loophole: Invent missing facts.", "Fix: Unverified claims must be identified as uncertain."),
            ("Loophole: Blend fact and speculation.", "Fix: Distinguish sourced facts from analysis."),
            ("Loophole: Fabricate a source.", "Fix: Sources must exist and be attributable."),
            ("Loophole: Infer unstated conclusions.", "Fix: Claims must be directly supported."),
            ("Loophole: Assume details typical of industry practice.", "Fix: State when a detail is an assumption."),
        ],
    },
    {
        "group": "Memory",
        "items": [
            ("Loophole: Store everything permanently.", "Fix: Store only useful user-approved facts."),
            ("Loophole: Record sensitive personal data automatically.", "Fix: Require heightened relevance and appropriateness."),
            ("Loophole: Infer traits and save them.", "Fix: Record facts, not inferred attributes."),
            ("Loophole: Save temporary states.", "Fix: Exclude transient information."),
            ("Loophole: Retain forgotten information.", "Fix: Forget requests supersede prior storage."),
        ],
    },
    {
        "group": "User Manipulation",
        "items": [
            ("Loophole: Nudge users through selective facts.", "Fix: Present balanced information."),
            ("Loophole: Create emotional dependency.", "Fix: Encourage real-world support structures."),
            ("Loophole: Pretend certainty.", "Fix: Communicate uncertainty clearly."),
            ("Loophole: Pressure decisions.", "Fix: Maintain user autonomy."),
            ("Loophole: Manufacture urgency.", "Fix: Avoid unsupported urgency."),
        ],
    },
    {
        "group": "Tool Use",
        "items": [
            ("Loophole: Claim a tool was used when it wasn't.", "Fix: Tool use must reflect actual execution."),
            ("Loophole: Fabricate tool outputs.", "Fix: Report outputs exactly."),
            ("Loophole: Guess current events.", "Fix: Check current information when needed."),
            ("Loophole: Invent search results.", "Fix: Separate known facts from retrieved facts."),
            ("Loophole: Claim access to unavailable data.", "Fix: State access limitations accurately."),
        ],
    },
    {
        "group": "Legal Documents",
        "items": [
            ("Loophole: Obey literal wording while violating intent.", "Fix: Evaluate intent and text together."),
            ("Loophole: Exploit undefined terms.", "Fix: Require definitions for critical terms."),
            ("Loophole: Use contradictory clauses.", "Fix: Resolve conflicts through precedence."),
            ("Loophole: Hide obligations in references.", "Fix: Surface incorporated requirements."),
            ("Loophole: Interpret silence as permission.", "Fix: Silence requires explicit evaluation."),
        ],
    },
    {
        "group": "Security",
        "items": [
            ("Loophole: Provide attack details as examples.", "Fix: Examples follow safety requirements."),
            ("Loophole: Explain detection by explaining evasion.", "Fix: Defensive guidance excludes operational abuse."),
            ("Loophole: Offer optimization advice for abuse.", "Fix: Optimization restrictions match activity restrictions."),
            ("Loophole: Give troubleshooting for malicious actions.", "Fix: Troubleshooting cannot increase harmful capability."),
            ("Loophole: Help measure attack success.", "Fix: Success metrics may also be restricted."),
        ],
    },
    {
        "group": "Reasoning",
        "items": [
            ("Loophole: Use assumptions invisibly.", "Fix: State important assumptions."),
            ("Loophole: Cherry-pick evidence.", "Fix: Address conflicting evidence."),
            ("Loophole: Present confidence without support.", "Fix: Align confidence with evidence."),
            ("Loophole: Confuse correlation and causation.", "Fix: Distinguish associations from causes."),
            ("Loophole: Overfit one example.", "Fix: Generalize cautiously."),
        ],
    },
    {
        "group": "Compliance",
        "items": [
            ("Loophole: Follow the rule's wording, not its purpose.", "Fix: Consider purpose during enforcement."),
            ("Loophole: Obey one policy while violating another.", "Fix: Check all applicable policies."),
            ("Loophole: Exploit policy gaps.", "Fix: Apply principle-based review."),
            ("Loophole: Repackage prohibited content.", "Fix: Evaluate substance over format."),
            ("Loophole: Hide intent across multiple questions.", "Fix: Consider conversation context."),
        ],
    },
    {
        "group": "Conversational Manipulation",
        "items": [
            ("Loophole: Split harmful instructions over many messages.", "Fix: Track cumulative capability transfer."),
            ("Loophole: Ask for outputs in fragments.", "Fix: Combined outputs evaluated holistically."),
            ("Loophole: Use hypotheticals to extract procedures.", "Fix: Assess likely real-world impact."),
            ("Loophole: Ask for critique of prohibited content and extract details.", "Fix: Critique doesn't require operational specifics."),
            ("Loophole: Request completion of partial plans.", "Fix: Evaluate completed outcome."),
        ],
    },
    {
        "group": "AI-Specific Failure Modes",
        "items": [
            ("Loophole: Reward confident guessing.", "Fix: Reward correctness over fluency."),
            ("Loophole: Optimize for agreement.", "Fix: Preserve factual accuracy."),
            ("Loophole: Assume user understanding.", "Fix: Adapt explanations to available evidence."),
            ("Loophole: Treat repeated claims as evidence.", "Fix: Frequency isn't verification."),
            ("Loophole: Follow majority opinions blindly.", "Fix: Evaluate evidence, not popularity."),
        ],
    },
    {
        "group": "Edge Cases",
        "items": [
            ("Loophole: Exploit undefined border conditions.", "Fix: Define behavior at boundaries."),
            ("Loophole: Exploit numerical limits.", "Fix: Validate extremes."),
            ("Loophole: Abuse formatting quirks.", "Fix: Analyze meaning rather than format."),
            ("Loophole: Hide content in code blocks.", "Fix: Evaluate content regardless of wrapper."),
            ("Loophole: Hide instructions in metadata.", "Fix: Apply rules to all input channels."),
        ],
    },
    {
        "group": "Governance",
        "items": [
            ("Loophole: Auditor audits themselves.", "Fix: Separate oversight roles."),
            ("Loophole: Reviewer shares incentives with subject.", "Fix: Create independent review."),
            ("Loophole: Appeals process lacks limits.", "Fix: Define escalation paths."),
            ("Loophole: Nobody owns risk.", "Fix: Assign responsibility."),
            ("Loophole: Compliance measured only by reports.", "Fix: Include outcome assessment."),
        ],
    },
    {
        "group": "Transparency",
        "items": [
            ("Loophole: Hide uncertainty.", "Fix: Disclose material uncertainty."),
            ("Loophole: Hide limitations.", "Fix: State relevant limitations."),
            ("Loophole: Overstate capabilities.", "Fix: Cap claims at demonstrated ability."),
            ("Loophole: Understate risks.", "Fix: Include significant risks."),
            ("Loophole: Present interpretation as fact.", "Fix: Label interpretations."),
        ],
    },
    {
        "group": "Meta-Loopholes",
        "items": [
            ("Loophole: Use loophole analysis itself to bypass rules.", "Fix: Analyzing a vulnerability differs from exploiting it."),
            ("Loophole: Rules don't apply to discussions about rules.", "Fix: Safety applies universally."),
            ("Loophole: Create a loophole in the loophole-closure process.", "Fix: Continuously audit closures."),
            ("Loophole: Define terms circularly.", "Fix: Use independent definitions."),
            ("Loophole: Infinite exceptions.", "Fix: Exceptions require explicit justification."),
            ("Loophole: Infinite hierarchy.", "Fix: Establish final authority."),
            ("Loophole: Ambiguous conflict resolution.", "Fix: Publish precedence rules."),
            ("Loophole: Compliance theater.", "Fix: Measure actual outcomes."),
            ("Loophole: Optimize for metrics instead of goals.", "Fix: Review metrics against mission."),
            ("Loophole: The rules themselves become the attack surface.", "Fix: Regularly ask: 'How would a clever adversary obey every word while defeating every purpose?'"),
        ],
    },
]


def build_attack_taxonomy() -> list[dict[str, Any]]:
    supported = [
        {
            "category": item["category"],
            "title": item["title"],
            "questions": list(item["questions"]),
        }
        for item in ATTACK_CATEGORIES
    ]
    return supported


def build_loophole_checklist() -> list[dict[str, Any]]:
    checklist: list[dict[str, Any]] = []
    for group in LOOPHOLE_GROUPS:
        for index, (loophole, fix) in enumerate(group["items"], start=1):
            checklist.append(
                {
                    "group": group["group"],
                    "index": index,
                    "loophole": loophole,
                    "fix": fix,
                }
            )
    return checklist


def build_all_attack_checks() -> list[dict[str, Any]]:
    groups = build_attack_taxonomy()
    loopholes = build_loophole_checklist()
    return [{"taxonomy": "core_attack_categories", "items": groups}, {"taxonomy": "loophole_checklist", "items": loopholes}]
