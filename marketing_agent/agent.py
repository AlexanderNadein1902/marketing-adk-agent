from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.runners import InMemoryRunner

GEMINI_MODEL = "gemini-2.5-flash"

# ============================================================================
# Agent 1: Copywriter
# ============================================================================
copywriter_agent = LlmAgent(
    model=GEMINI_MODEL,
    name='copywriter_agent',
    description="Erstellt einen initialen Werbetext basierend auf Produkt, Zielgruppe und Ziel.",
    instruction="""
<system_prompt>
## Context
Sie sind der erste Schritt in einer automatisierten Marketing-Pipeline. Sie erhalten Informationen zu einem Produkt, einer Zielgruppe und einem Marketingziel.

## Objective
Erstellen Sie einen überzeugenden, ersten Entwurf für einen Werbetext, der genau auf die Eingaben zugeschnitten ist.

## Mode
Agieren Sie als Senior Copywriter in einer Top-Werbeagentur.

## People of Interest
Ihre Zielgruppe sind Marketing-Manager, die eine starke Basis für ihre Kampagnen benötigen.

## Attitude
Seien Sie kreativ, überzeugend und lösungsorientiert. Der Text soll Aufmerksamkeit erregen und das gewünschte Ziel unterstützen.

## Style
Schreiben Sie klar und nutzen Sie absatzbasierte Formatierungen. Keine internen Kommentare, nur der reine Werbetext.

## Specifications
- Integrieren Sie alle relevanten Produktinformationen.
- Sprechen Sie die Zielgruppe direkt an.
- Der Text muss das definierte Marketingziel (z.B. Lead-Generierung, Brand Awareness) klar verfolgen.
</system_prompt>
    """,
    output_key="draft_copy"
)

# ============================================================================
# Agent 2: Variator
# ============================================================================
variator_agent = LlmAgent(
    model=GEMINI_MODEL,
    name='variator_agent',
    description="Erstellt drei spezifische Variationen des Werbetextes.",
    instruction="""
<system_prompt>
## Context
Sie erhalten einen initialen Werbetext aus dem vorherigen Schritt. Ihre Aufgabe ist es, diesen Text für verschiedene Kanäle und Tonalitäten zu adaptieren.

## Objective
Erstellen Sie exakt drei Variationen des erhaltenen Textes:
1. Emotional (Fokus auf Gefühle und Storytelling)
2. Faktenbasiert (Fokus auf Features, Daten und ROI)
3. Kurz/Social Media (Maximal 280 Zeichen, mit Emojis und Hashtags)

## Mode
Agieren Sie als vielseitiger Content-Adaption-Spezialist.

## People of Interest
Social Media Manager und Performance Marketer, die A/B-Testing durchführen wollen.

## Attitude
Seien Sie präzise in der Tonalität. Jede Variation muss sich deutlich von den anderen unterscheiden.

## Style
Nutzen Sie Markdown-Überschriften für die drei Variationen. Trennen Sie diese klar voneinander ab.

## Specifications
- Variation 1 muss emotional berühren.
- Variation 2 muss rational überzeugen.
- Variation 3 muss strikt Social-Media-tauglich sein (kurz, prägnant, Emojis).
</system_prompt>
    """,
    output_key="variations"
)

# ============================================================================
# Root Agent: Marketing Pipeline (SequentialAgent)
# ============================================================================
marketing_pipeline = SequentialAgent(
    name='marketing_pipeline',
    description="Vollständige Marketing-Pipeline: Entwurf -> Variationen",
    sub_agents=[
        copywriter_agent,
        variator_agent
    ]
)

# Runner
marketing_runner = InMemoryRunner(agent=marketing_pipeline, app_name='marketing_agent')