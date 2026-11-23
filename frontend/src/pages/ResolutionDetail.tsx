import React from "react";
import { useNavigate } from "react-router-dom";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";
import { CrudButton } from "../components/runtime/CrudButton";

const ResolutionDetail: React.FC = () => {
  const navigate = useNavigate();
  return (
    <div id="page-resolution-detail" style={{
                "fontFamily": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
                "minHeight": "100vh",
                "background": "#f7f6fb",
                "color": "#23213a",
                "--chart-color-palette": "default"
              }}>
    <nav id="ieptgy" className="assistant-nav-header" style={{
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
      <p id="iakp0c" style={{"fontSize": "1.25rem", "fontWeight": "700", "letterSpacing": "-0.01em", "color": "#23213a", "--chart-color-palette": "default"}}>{"Stride"}</p>
      <div id="igz7iz" style={{"display": "flex", "--chart-color-palette": "default", "alignItems": "center", "gap": "4px"}}>
        <a id="ivh6af" style={{
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
        <a id="iy0dwt" style={{
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
        <a id="ii0ae1" style={{
            "padding": "8px 16px",
            "fontSize": "0.9rem",
            "fontWeight": "600",
            "textDecoration": "none",
            "transition": "all 0.2s",
            "background": "rgba(85, 70, 217, 0.1)",
            "color": "#5546d9",
            "borderRadius": "16px",
            "--chart-color-palette": "default"
          }} onClick={(e) => { if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; e.preventDefault(); navigate("/resolution-detail"); }} href="/resolution-detail" {...{"data-navigate-to": "resolution-detail"}}>{"Resolution Detail"}</a>
        <a id="iksifc" style={{
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
        <a id="ivi1c5" style={{
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
    <main id="iyrx2m" className="assistant-main" style={{"padding": "24px 16px", "margin": "0 auto", "maxWidth": "1200px", "--chart-color-palette": "default"}}>
      <header id="container_header_3" className="app-head">
        <div id="Component_17">
          <p id="p_11" className="app-eyebrow">{"GOAL WORKSPACE"}</p>
          <h1 id="h1_3">{"Keep the goal moving."}</h1>
          <p id="p_12">{"Manage milestones and record the actions behind your progress."}</p>
        </div>
        <div id="a_6" className="app-link" {...{"href": "/resolutions"}}>{"← All resolutions"}</div>
      </header>
      <section id="container_section_9" className="app-band">
        <div id="Component_18">
          <h2 id="h2_8">{"Break it down. Build it up."}</h2>
          <p id="p_13">{"Small milestones give your bigger goal a path forward."}</p>
        </div>
        <div id="a_7" {...{"href": "/habits"}}>{"Explore habits →"}</div>
      </section>
      <section id="container_section_10" className="app-wrap">
        <h2 id="h2_9" className="app-section-title">{"Goal details"}</h2>
        <div id="Component_19" className="app-panel app-table">
          <TableBlock id="table-resolution-resolution-detail" styles={{"width": "100%", "margin": "12px 0", "minHeight": "300px", "borderRadius": "12px", "--chart-color-palette": "default"}} title="Goal details and status" options={{
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
        <div id="Component_20" className="app-actions">
          <MethodButton id="action_button_4" className="action-button-component" endpoint="/resolution/{resolution_id}/methods/activate/" label="Activate selectedActivate selected" isInstanceMethod={true} instanceSourceTableId="table-resolution-resolution-detail" />
          <MethodButton id="action_button_5" className="action-button-component" endpoint="/resolution/{resolution_id}/methods/pause/" label="Pause selectedPause selected" isInstanceMethod={true} instanceSourceTableId="table-resolution-resolution-detail" />
          <MethodButton id="action_button_6" className="action-button-component" endpoint="/resolution/{resolution_id}/methods/complete/" label="Complete selectedComplete selected" isInstanceMethod={true} instanceSourceTableId="table-resolution-resolution-detail" />
          <MethodButton id="action_button_7" className="action-button-component" endpoint="/progressentry/{progressentry_id}/methods/edit/" label="Edit ResolutionEdit Resolution" parameters={[{"name": "notes", "type": "str", "required": true}, {"name": "amount", "type": "float", "required": true}]} isInstanceMethod={true} instanceSourceTableId="table-progressentry-resolution-detail" />
        </div>
      </section>
      <section id="container_section_11" className="app-wrap">
        <h2 id="h2_10" className="app-section-title">{"Milestones"}</h2>
        <p id="p_14" className="app-section-sub">{"Select a milestone to mark it complete."}</p>
        <div id="Component_21" className="app-panel app-table">
          <TableBlock id="table-subgoal-resolution-detail" styles={{"width": "100%", "margin": "12px 0", "minHeight": "300px", "borderRadius": "12px", "--chart-color-palette": "default"}} title="Goal milestones" options={{
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
                  "label": "Target date",
                  "column_type": "field",
                  "field": "targetDate",
                  "type": "date",
                  "required": true
                },
                {
                  "label": "Completed",
                  "column_type": "field",
                  "field": "completed",
                  "type": "bool",
                  "required": true
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
                  "field": "completed",
                  "label": "completed",
                  "type": "bool",
                  "required": true,
                  "defaultValue": null
                },
                {
                  "column_type": "lookup",
                  "path": "parentResolution",
                  "field": "parentResolution",
                  "lookup_field": "title",
                  "target_field": "id",
                  "target_type": "int",
                  "entity": "Resolution",
                  "type": "str",
                  "required": true
                }
              ]
            }} dataBinding={{"entity": "SubGoal", "endpoint": "/subgoal/", "row_key_fields": ["id"]}} />
        </div>
        <div id="Component_22" className="app-actions">
          <MethodButton id="action_button_8" className="action-button-component" endpoint="/subgoal/{subgoal_id}/methods/markComplete/" label="Complete selected milestoneComplete selected milestone" isInstanceMethod={true} instanceSourceTableId="table-subgoal-resolution-detail" />
          <CrudButton id="action_button_9" className="action-button-component" label="Add SubGoalAdd SubGoal" action="create" tableId="table-subgoal-resolution-detail" entity="SubGoal" />
        </div>
      </section>
      <section id="container_section_12" className="app-wrap">
        <h2 id="h2_11" className="app-section-title">{"Progress entries"}</h2>
        <p id="p_15" className="app-section-sub">{"Select an entry to edit or remove it."}</p>
        <div id="Component_23" className="app-panel app-table">
          <TableBlock id="table-progressentry-resolution-detail" styles={{"width": "100%", "margin": "12px 0", "minHeight": "300px", "borderRadius": "12px", "--chart-color-palette": "default"}} title="Recorded progress" options={{
              "showHeader": true,
              "stripedRows": false,
              "showPagination": true,
              "rowsPerPage": 5,
              "actionButtons": true,
              "columns": [
                {
                  "label": "Date",
                  "column_type": "field",
                  "field": "date",
                  "type": "datetime",
                  "required": true
                },
                {
                  "label": "Notes",
                  "column_type": "field",
                  "field": "notes",
                  "type": "str",
                  "required": true
                },
                {
                  "label": "Amount",
                  "column_type": "field",
                  "field": "amount",
                  "type": "float",
                  "required": true
                },
                {
                  "label": "Resolution",
                  "column_type": "lookup",
                  "path": "resolution",
                  "entity": "Resolution",
                  "field": "title",
                  "type": "str",
                  "required": false
                },
                {
                  "label": "Habit",
                  "column_type": "lookup",
                  "path": "habit",
                  "entity": "Habit",
                  "field": "name",
                  "type": "str",
                  "required": false
                }
              ],
              "formColumns": [
                {
                  "column_type": "field",
                  "field": "date",
                  "label": "date",
                  "type": "datetime",
                  "required": true,
                  "defaultValue": null
                },
                {
                  "column_type": "field",
                  "field": "notes",
                  "label": "notes",
                  "type": "str",
                  "required": false,
                  "defaultValue": null
                },
                {
                  "column_type": "field",
                  "field": "amount",
                  "label": "amount",
                  "type": "float",
                  "required": false,
                  "defaultValue": null
                },
                {
                  "column_type": "lookup",
                  "path": "resolution",
                  "field": "resolution",
                  "lookup_field": "title",
                  "target_field": "id",
                  "target_type": "int",
                  "entity": "Resolution",
                  "type": "str",
                  "required": false
                },
                {
                  "column_type": "lookup",
                  "path": "habit",
                  "field": "habit",
                  "lookup_field": "name",
                  "target_field": "id",
                  "target_type": "int",
                  "entity": "Habit",
                  "type": "str",
                  "required": false
                },
                {
                  "column_type": "lookup",
                  "path": "author",
                  "field": "author",
                  "lookup_field": "email",
                  "target_field": "id",
                  "target_type": "int",
                  "entity": "User",
                  "type": "str",
                  "required": true
                }
              ]
            }} dataBinding={{"entity": "ProgressEntry", "endpoint": "/progressentry/", "row_key_fields": ["id"]}} />
        </div>
        <div id="Component_24" className="app-actions">
          <MethodButton id="action_button_10" className="action-button-component" endpoint="/progressentry/{progressentry_id}/methods/edit/" label="Edit selected entryEdit selected entry" parameters={[{"name": "notes", "type": "str", "required": true}, {"name": "amount", "type": "float", "required": true}]} isInstanceMethod={true} instanceSourceTableId="table-progressentry-resolution-detail" />
          <MethodButton id="action_button_11" className="action-button-component" endpoint="/progressentry/{progressentry_id}/methods/remove/" label="Remove selected entryRemove selected entry" isInstanceMethod={true} instanceSourceTableId="table-progressentry-resolution-detail" />
          <CrudButton id="action_button_12" className="action-button-component" label="Add ProgressEntryAdd ProgressEntry" action="create" tableId="table-progressentry-resolution-detail" entity="ProgressEntry" />
        </div>
      </section>
    </main>    </div>
  );
};

export default ResolutionDetail;
