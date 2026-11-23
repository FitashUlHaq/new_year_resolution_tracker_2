import React from "react";
import { useNavigate } from "react-router-dom";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Habits: React.FC = () => {
  const navigate = useNavigate();
  return (
    <div id="page-habits" style={{
              "fontFamily": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
              "minHeight": "100vh",
              "background": "#f7f6fb",
              "color": "#23213a",
              "--chart-color-palette": "default"
            }}>
    <nav id="idqzk4" className="assistant-nav-header" style={{
        "height": "64px",
        "padding": "0 32px",
        "fontFamily": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
        "position": "sticky",
        "top": "0",
        "zIndex": 50,
        "display": "flex",
        "background": "#ffffff",
        "borderBottom": "1px solid #e8e5f0",
        "boxShadow": "0 1px 3px rgba(0,0,0,0.06)",
        "--chart-color-palette": "default",
        "justifyContent": "space-between",
        "alignItems": "center"
      }}>
      <p id="it0pbf" style={{"fontSize": "1.25rem", "fontWeight": "700", "letterSpacing": "-0.01em", "color": "#23213a", "--chart-color-palette": "default"}}>{"Stride"}</p>
      <div id="ictloj" style={{"display": "flex", "--chart-color-palette": "default", "alignItems": "center", "gap": "4px"}}>
        <a id="ijx9yk" style={{
            "padding": "8px 16px",
            "fontSize": "0.9rem",
            "fontWeight": "500",
            "textDecoration": "none",
            "transition": "all 0.2s",
            "background": "transparent",
            "color": "#69667e",
            "borderRadius": "16px",
            "--chart-color-palette": "default"
          }} onClick={(e) => { if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; e.preventDefault(); navigate("/dashboard"); }} href="/dashboard" {...{"data-navigate-to": "dashboard"}}>{"Dashboard"}</a>
        <a id="iak08s" style={{
            "padding": "8px 16px",
            "fontSize": "0.9rem",
            "fontWeight": "500",
            "textDecoration": "none",
            "transition": "all 0.2s",
            "background": "transparent",
            "color": "#69667e",
            "borderRadius": "16px",
            "--chart-color-palette": "default"
          }} onClick={(e) => { if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; e.preventDefault(); navigate("/resolutions"); }} href="/resolutions" {...{"data-navigate-to": "resolutions"}}>{"Resolutions"}</a>
        <a id="itvn7j" style={{
            "padding": "8px 16px",
            "fontSize": "0.9rem",
            "fontWeight": "500",
            "textDecoration": "none",
            "transition": "all 0.2s",
            "background": "transparent",
            "color": "#69667e",
            "borderRadius": "16px",
            "--chart-color-palette": "default"
          }} onClick={(e) => { if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; e.preventDefault(); navigate("/resolution-detail"); }} href="/resolution-detail" {...{"data-navigate-to": "resolution-detail"}}>{"Resolution Detail"}</a>
        <a id="i8gedk" style={{
            "padding": "8px 16px",
            "fontSize": "0.9rem",
            "fontWeight": "600",
            "textDecoration": "none",
            "transition": "all 0.2s",
            "background": "rgba(85, 70, 217, 0.1)",
            "color": "#5546d9",
            "borderRadius": "16px",
            "--chart-color-palette": "default"
          }} onClick={(e) => { if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; e.preventDefault(); navigate("/habits"); }} href="/habits" {...{"data-navigate-to": "habits"}}>{"Habits"}</a>
        <a id="itulre" style={{
            "padding": "8px 16px",
            "fontSize": "0.9rem",
            "fontWeight": "500",
            "textDecoration": "none",
            "transition": "all 0.2s",
            "background": "transparent",
            "color": "#69667e",
            "borderRadius": "16px",
            "--chart-color-palette": "default"
          }} onClick={(e) => { if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; e.preventDefault(); navigate("/categories-profile"); }} href="/categories-profile" {...{"data-navigate-to": "categories-profile"}}>{"Categories & Profile"}</a>
      </div>
    </nav>
    <main id="iap5mt" className="assistant-main" style={{"padding": "24px 16px", "margin": "0 auto", "maxWidth": "1200px", "--chart-color-palette": "default"}}>
      <header id="container_header_4" className="app-head">
        <div id="Component_25">
          <p id="p_16" className="app-eyebrow">{"SHOW UP AGAIN"}</p>
          <h1 id="h1_4">{"Build your rhythm."}</h1>
          <p id="p_17">{"Track the routines that make progress feel possible."}</p>
        </div>
        <div id="a_8" className="app-link" {...{"href": "/dashboard"}}>{"Back to overview"}</div>
      </header>
      <section id="container_section_13" className="app-band">
        <div id="Component_26">
          <h2 id="h2_12">{"Consistency has a shape."}</h2>
          <p id="p_18">{"Mark a habit done, then watch your streak reflect the work you put in."}</p>
        </div>
        <div id="a_9" {...{"href": "/resolutions"}}>{"See your goals →"}</div>
      </section>
      <section id="container_section_14" className="app-wrap">
        <h2 id="h2_13" className="app-section-title">{"Your habits"}</h2>
        <p id="p_19" className="app-section-sub">{"Select a habit to mark it done or reset its streak."}</p>
        <div id="Component_27" className="app-panel app-table">
          <TableBlock id="table-habit-habits" styles={{"width": "100%", "margin": "12px 0", "minHeight": "300px", "borderRadius": "12px", "--chart-color-palette": "default"}} title="Habit routines and streaks" options={{
              "showHeader": true,
              "stripedRows": false,
              "showPagination": true,
              "rowsPerPage": 5,
              "actionButtons": true,
              "columns": [
                {
                  "label": "Name",
                  "column_type": "field",
                  "field": "name",
                  "type": "str",
                  "required": true
                },
                {
                  "label": "Description",
                  "column_type": "field",
                  "field": "description",
                  "type": "str",
                  "required": true
                },
                {
                  "label": "Created at",
                  "column_type": "field",
                  "field": "createdAt",
                  "type": "datetime",
                  "required": true
                },
                {
                  "label": "Frequency",
                  "column_type": "field",
                  "field": "frequency",
                  "type": "enum",
                  "options": [
                    "DAILY",
                    "MONTHLY",
                    "WEEKLY",
                    "YEARLY"
                  ],
                  "required": true
                },
                {
                  "label": "Active",
                  "column_type": "field",
                  "field": "active",
                  "type": "bool",
                  "required": true
                },
                {
                  "label": "Current streak",
                  "column_type": "field",
                  "field": "currentStreak",
                  "type": "int",
                  "required": true
                },
                {
                  "label": "Last done at",
                  "column_type": "field",
                  "field": "lastDoneAt",
                  "type": "datetime",
                  "required": true
                }
              ],
              "formColumns": [
                {
                  "column_type": "field",
                  "field": "name",
                  "label": "name",
                  "type": "str",
                  "required": true,
                  "defaultValue": null
                },
                {
                  "column_type": "field",
                  "field": "description",
                  "label": "description",
                  "type": "str",
                  "required": false,
                  "defaultValue": null
                },
                {
                  "column_type": "field",
                  "field": "frequency",
                  "label": "frequency",
                  "type": "enum",
                  "required": true,
                  "defaultValue": null,
                  "options": [
                    "DAILY",
                    "MONTHLY",
                    "WEEKLY",
                    "YEARLY"
                  ]
                },
                {
                  "column_type": "field",
                  "field": "active",
                  "label": "active",
                  "type": "bool",
                  "required": true,
                  "defaultValue": null
                },
                {
                  "column_type": "field",
                  "field": "currentStreak",
                  "label": "currentStreak",
                  "type": "int",
                  "required": true,
                  "defaultValue": null
                },
                {
                  "column_type": "field",
                  "field": "lastDoneAt",
                  "label": "lastDoneAt",
                  "type": "datetime",
                  "required": false,
                  "defaultValue": null
                },
                {
                  "column_type": "lookup",
                  "path": "progressEntries",
                  "field": "progressEntries",
                  "lookup_field": "notes",
                  "target_field": "id",
                  "target_type": "int",
                  "entity": "ProgressEntry",
                  "type": "list",
                  "required": false
                },
                {
                  "column_type": "lookup",
                  "path": "habitUser",
                  "field": "habitUser",
                  "lookup_field": "email",
                  "target_field": "id",
                  "target_type": "int",
                  "entity": "User",
                  "type": "str",
                  "required": true
                }
              ]
            }} dataBinding={{"entity": "Habit", "endpoint": "/habit/", "row_key_fields": ["id"]}} />
        </div>
        <div id="Component_28" className="app-actions">
          <MethodButton id="action_button_13" className="action-button-component" endpoint="/habit/{habit_id}/methods/markDone/" label="Mark selected doneMark selected done" parameters={[{"name": "doneAt", "type": "datetime", "required": true}]} isInstanceMethod={true} instanceSourceTableId="table-habit-habits" />
          <MethodButton id="action_button_14" className="action-button-component" endpoint="/habit/{habit_id}/methods/resetStreak/" label="Reset selected streakReset selected streak" isInstanceMethod={true} instanceSourceTableId="table-habit-habits" />
        </div>
      </section>
      <section id="container_section_15" className="app-wrap">
        <h2 id="h2_14" className="app-section-title">{"Add a habit"}</h2>
        <div id="Component_29" className="app-panel app-accent">
          <p id="p_20">{"Choose a name and frequency for the routine you want to practice."}</p>
          <form id="form_2" className="app-form" onSubmit={(e) => { e.preventDefault(); }}>
            <div style={{"marginBottom": "16px"}}>
            <label htmlFor="h_name" style={{"display": "block", "marginBottom": "5px", "fontWeight": "500"}}>{"Name"}<span style={{"color": "#ef4444", "marginLeft": "2px"}}>*</span></label>
            <input type="text" id="h_name" style={{"padding": "6px 10px", "border": "1px solid #cbd5e1", "borderRadius": "4px", "fontFamily": "inherit", "width": "100%", "boxSizing": "border-box"}} required={true} />
            </div>
            <div style={{"marginBottom": "16px"}}>
            <label htmlFor="h_frequency" style={{"display": "block", "marginBottom": "5px", "fontWeight": "500"}}>{"Frequency: DAILY, WEEKLY, MONTHLY or YEARLY"}<span style={{"color": "#ef4444", "marginLeft": "2px"}}>*</span></label>
            <input type="text" id="h_frequency" style={{"padding": "6px 10px", "border": "1px solid #cbd5e1", "borderRadius": "4px", "fontFamily": "inherit", "width": "100%", "boxSizing": "border-box"}} required={true} />
            </div>
            <div style={{"marginBottom": "16px"}}>
            <label htmlFor="h_description" style={{"display": "block", "marginBottom": "5px", "fontWeight": "500"}}>{"Description"}</label>
            <input type="text" id="h_description" style={{"padding": "6px 10px", "border": "1px solid #cbd5e1", "borderRadius": "4px", "fontFamily": "inherit", "width": "100%", "boxSizing": "border-box"}} />
            </div>
            <div style={{"marginBottom": "16px"}}>
            <label htmlFor="h_active" style={{"display": "block", "marginBottom": "5px", "fontWeight": "500"}}>{"Active: true or false"}</label>
            <input type="text" id="h_active" style={{"padding": "6px 10px", "border": "1px solid #cbd5e1", "borderRadius": "4px", "fontFamily": "inherit", "width": "100%", "boxSizing": "border-box"}} />
            </div>
            <button type="submit">{"Create habit"}</button>
          </form>
        </div>
      </section>
    </main>    </div>
  );
};

export default Habits;
