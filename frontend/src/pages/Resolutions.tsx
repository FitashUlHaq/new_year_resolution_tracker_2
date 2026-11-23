import React from "react";
import { useNavigate } from "react-router-dom";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Resolutions: React.FC = () => {
  const navigate = useNavigate();
  return (
    <div id="page-resolutions" style={{
              "fontFamily": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
              "minHeight": "100vh",
              "background": "#f7f6fb",
              "color": "#23213a",
              "--chart-color-palette": "default"
            }}>
    <nav id="i7rsd" className="assistant-nav-header" style={{
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
      <p id="i6gek" style={{"fontSize": "1.25rem", "fontWeight": "700", "letterSpacing": "-0.01em", "color": "#23213a", "--chart-color-palette": "default"}}>{"Stride"}</p>
      <div id="iozdl" style={{"display": "flex", "--chart-color-palette": "default", "alignItems": "center", "gap": "4px"}}>
        <a id="itnti" style={{
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
        <a id="i4iok" style={{
            "padding": "8px 16px",
            "fontSize": "0.9rem",
            "fontWeight": "600",
            "textDecoration": "none",
            "transition": "all 0.2s",
            "background": "rgba(85, 70, 217, 0.1)",
            "color": "#5546d9",
            "borderRadius": "16px",
            "--chart-color-palette": "default"
          }} onClick={(e) => { if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; e.preventDefault(); navigate("/resolutions"); }} href="/resolutions" {...{"data-navigate-to": "resolutions"}}>{"Resolutions"}</a>
        <a id="i4ltd" style={{
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
        <a id="ic2si" style={{
            "padding": "8px 16px",
            "fontSize": "0.9rem",
            "fontWeight": "500",
            "textDecoration": "none",
            "transition": "all 0.2s",
            "background": "transparent",
            "color": "#69667e",
            "borderRadius": "16px",
            "--chart-color-palette": "default"
          }} onClick={(e) => { if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; e.preventDefault(); navigate("/habits"); }} href="/habits" {...{"data-navigate-to": "habits"}}>{"Habits"}</a>
        <a id="i49yw" style={{
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
    <main id="i3qig" className="assistant-main" style={{"padding": "24px 16px", "margin": "0 auto", "maxWidth": "1200px", "--chart-color-palette": "default"}}>
      <header id="container_header_2" className="app-head">
        <div id="Component_9">
          <p id="p_7" className="app-eyebrow">{"DIRECTION, NOT PERFECTION"}</p>
          <h1 id="h1_2">{"Your resolutions"}</h1>
          <p id="p_8">{"Shape what matters, then keep each goal moving at your pace."}</p>
        </div>
        <div id="a_4" className="ds-btn ds-btn-primary" {...{"href": "/resolution-detail"}}>{"View goal workspace"}</div>
      </header>
      <section id="container_section_7" className="app-wrap">
        <h2 id="h2_6" className="app-section-title">{"All resolutions"}</h2>
        <p id="p_9" className="app-section-sub">{"Select a row to use its actions. Open the goal workspace to manage milestones and progress."}</p>
        <div id="Component_10" className="app-panel app-table">
          <TableBlock id="table-resolution-resolutions" styles={{"width": "100%", "margin": "12px 0", "minHeight": "300px", "borderRadius": "12px", "--chart-color-palette": "default"}} title="Your resolutions and target dates" options={{
              "showHeader": true,
              "stripedRows": false,
              "showPagination": true,
              "rowsPerPage": 5,
              "actionButtons": true,
              "columns": [
                {
                  "label": "Title",
                  "column_type": "field",
                  "field": "title",
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
                  "label": "Updated at",
                  "column_type": "field",
                  "field": "updatedAt",
                  "type": "datetime",
                  "required": true
                },
                {
                  "label": "Target date",
                  "column_type": "field",
                  "field": "targetDate",
                  "type": "date",
                  "required": true
                },
                {
                  "label": "Status",
                  "column_type": "field",
                  "field": "status",
                  "type": "enum",
                  "options": [
                    "ABANDONED",
                    "ACTIVE",
                    "COMPLETED",
                    "PAUSED",
                    "PLANNED"
                  ],
                  "required": true
                },
                {
                  "label": "Category",
                  "column_type": "lookup",
                  "path": "category",
                  "entity": "Category",
                  "field": "name",
                  "type": "str",
                  "required": false
                }
              ],
              "formColumns": [
                {
                  "column_type": "field",
                  "field": "title",
                  "label": "title",
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
                  "field": "targetDate",
                  "label": "targetDate",
                  "type": "date",
                  "required": false,
                  "defaultValue": null
                },
                {
                  "column_type": "field",
                  "field": "status",
                  "label": "status",
                  "type": "enum",
                  "required": true,
                  "defaultValue": null,
                  "options": [
                    "ABANDONED",
                    "ACTIVE",
                    "COMPLETED",
                    "PAUSED",
                    "PLANNED"
                  ]
                },
                {
                  "column_type": "lookup",
                  "path": "owner",
                  "field": "owner",
                  "lookup_field": "email",
                  "target_field": "id",
                  "target_type": "int",
                  "entity": "User",
                  "type": "str",
                  "required": true
                },
                {
                  "column_type": "lookup",
                  "path": "subGoals",
                  "field": "subGoals",
                  "lookup_field": "title",
                  "target_field": "id",
                  "target_type": "int",
                  "entity": "SubGoal",
                  "type": "list",
                  "required": false
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
                  "path": "category",
                  "field": "category",
                  "lookup_field": "name",
                  "target_field": "id",
                  "target_type": "int",
                  "entity": "Category",
                  "type": "str",
                  "required": false
                }
              ]
            }} dataBinding={{"entity": "Resolution", "endpoint": "/resolution/", "row_key_fields": ["id"]}} />
        </div>
        <div id="Component_11" className="app-actions">
          <MethodButton id="action_button" className="action-button-component" endpoint="/resolution/{resolution_id}/methods/activate/" label="Activate selectedActivate selected" isInstanceMethod={true} instanceSourceTableId="table-resolution-resolutions" />
          <MethodButton id="action_button_2" className="action-button-component" endpoint="/resolution/{resolution_id}/methods/pause/" label="Pause selectedPause selected" isInstanceMethod={true} instanceSourceTableId="table-resolution-resolutions" />
          <MethodButton id="action_button_3" className="action-button-component" endpoint="/resolution/{resolution_id}/methods/complete/" label="Complete selectedComplete selected" isInstanceMethod={true} instanceSourceTableId="table-resolution-resolutions" />
          <div id="a_5" {...{"href": "/resolution-detail"}}>{"Open goal workspace →"}</div>
        </div>
      </section>
      <section id="container_section_8" className="app-wrap">
        <h2 id="h2_7" className="app-section-title">{"Start a new resolution"}</h2>
        <div id="Component_12" className="app-panel app-accent">
          <p id="p_10">{"Give your goal a clear name and a target date. You can track its steps and progress in the goal workspace."}</p>
          <form id="form" className="app-form" onSubmit={(e) => { e.preventDefault(); }}>
            <div style={{"marginBottom": "16px"}}>
            <label htmlFor="r_title" style={{"display": "block", "marginBottom": "5px", "fontWeight": "500"}}>{"Title"}<span style={{"color": "#ef4444", "marginLeft": "2px"}}>*</span></label>
            <input type="text" id="r_title" style={{"padding": "6px 10px", "border": "1px solid #cbd5e1", "borderRadius": "4px", "fontFamily": "inherit", "width": "100%", "boxSizing": "border-box"}} required={true} />
            </div>
            <div style={{"marginBottom": "16px"}}>
            <label htmlFor="r_date" style={{"display": "block", "marginBottom": "5px", "fontWeight": "500"}}>{"Target date"}</label>
            <input type="date" id="r_date" style={{"padding": "6px 10px", "border": "1px solid #cbd5e1", "borderRadius": "4px", "fontFamily": "inherit", "width": "100%", "boxSizing": "border-box"}} />
            </div>
            <div style={{"marginBottom": "16px"}}>
            <label htmlFor="r_description" style={{"display": "block", "marginBottom": "5px", "fontWeight": "500"}}>{"Description"}</label>
            <input type="text" id="r_description" style={{"padding": "6px 10px", "border": "1px solid #cbd5e1", "borderRadius": "4px", "fontFamily": "inherit", "width": "100%", "boxSizing": "border-box"}} />
            </div>
            <button type="submit">{"Create resolution"}</button>
          </form>
        </div>
      </section>
    </main>    </div>
  );
};

export default Resolutions;
