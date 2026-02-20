import gradio as gr
import asyncio
from uuid import uuid4
from dotenv import load_dotenv
from google.genai import types

# Import root agent runner
from marketing_agent.agent import marketing_runner

load_dotenv()

async def run_marketing_pipeline_async(product: str, audience: str, goal: str, keywords: str):
    """
    Führt die vollständige Marketing-Pipeline asynchron aus.
    """
    try:
        session = await marketing_runner.session_service.create_session(
            user_id='user',
            app_name='marketing_agent'
        )
    except TypeError:
        session = await marketing_runner.session_service.create_session(
            app_name='marketing_agent',
            user_id='user',
            session_id=str(uuid4())
        )

    # Konstruiere den initialen Prompt aus den strukturierten Eingaben
    combined_prompt = f"""
    Produkt/Dienstleistung: {product}
    Zielgruppe: {audience}
    Marketingziel: {goal}
    Wichtige Keywords: {keywords}
    
    Bitte erstelle den initialen Werbetext.
    """

    content = types.Content(
        role='user',
        parts=[types.Part(text=combined_prompt)]
    )

    events_async = marketing_runner.run_async(
        user_id='user',
        session_id=session.id,
        new_message=content
    )

    if hasattr(events_async, "__await__"):
        events_async = await events_async

    results = {}
    async for event in events_async:
        if event.actions and event.actions.state_delta:
            for key, value in event.actions.state_delta.items():
                results[key] = value

    return results

def process_request(product: str, audience: str, goal: str, keywords: str):
    """Synchroner Wrapper für Gradio."""
    try:
        if not product or not audience or not goal:
            return "Fehler: Bitte füllen Sie alle Pflichtfelder aus.", ""
            
        results = asyncio.run(
            run_marketing_pipeline_async(product, audience, goal, keywords)
        )
        
        draft = results.get('draft_copy', 'Kein Entwurf generiert.')
        variations = results.get('variations', 'Keine Variationen generiert.')
        
        return draft, variations
    except Exception as e:
        error_msg = f"Fehler bei der Ausführung: {str(e)}"
        return error_msg, error_msg

# ============================================================================
# Gradio UI
# ============================================================================

with gr.Blocks(title="AI Marketing Copywriter") as demo:
    gr.Markdown("""
    # 🚀 AI Marketing Agent (Google ADK)
    
    Diese Pipeline nutzt den **SequentialAgent** zur Erstellung hochwertiger Werbetexte:
    1. **Copywriter Agent** → Erstellt den initialen Entwurf.
    2. **Variator Agent** → Erzeugt emotionale, faktenbasierte und Social-Media-Varianten.
    """)

    with gr.Row():
        with gr.Column():
            product_input = gr.Textbox(label="Produkt / Dienstleistung (*)", placeholder="z.B. Eco-Friendly Kaffeemaschine", lines=2)
            audience_input = gr.Textbox(label="Zielgruppe (*)", placeholder="z.B. Umweltbewusste Millennials", lines=2)
        with gr.Column():
            goal_input = gr.Textbox(label="Marketingziel (*)", placeholder="z.B. Vorbestellungen generieren (Lead Gen)", lines=2)
            keyword_input = gr.Textbox(label="Wichtige Keywords (optional)", placeholder="z.B. nachhaltig, fairtrade, innovativ", lines=2)

    submit_btn = gr.Button("Kampagne generieren", variant="primary")

    gr.Markdown("## 📋 Ergebnisse")

    with gr.Row():
        gr.Markdown("### Entwurf (Copywriter)")
        draft_output = gr.Markdown(value="*Warte auf Eingabe...*")
        
    with gr.Row():
        gr.Markdown("### Variationen (Variator)")
        variations_output = gr.Markdown(value="*Warte auf Eingabe...*")

    submit_btn.click(
        fn=process_request,
        inputs=[product_input, audience_input, goal_input, keyword_input],
        outputs=[draft_output, variations_output]
    )

if __name__ == "__main__":
    demo.launch()

