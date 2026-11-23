import React from "react";
import { useNavigate } from "react-router-dom";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";
import { CrudButton } from "../components/runtime/CrudButton";

const CategoriesProfile: React.FC = () => {
  const navigate = useNavigate();
  return (
    <div id="page-categories-profile" style={{
    "fontFamily": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    "minHeight": "100vh",
    "background": "#f7f6fb",
    "color": "#23213a",
    "--chart-color-palette": "default"
  }}>
    <nav id="icyl7o" className="assistant-nav-header" style={{
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
      <p id="ia7sgz" style={{"fontSize": "1.25rem", "fontWeight": "700", "letterSpacing": "-0.01em", "color": "#23213a", "--chart-color-palette": "default"}}>{"Stride"}</p>
      <div id="ifxfhl" style={{"display": "flex", "--chart-color-palette": "default", "alignItems": "center", "gap": "4px"}}>
        <a id="iheo7o" style={{
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
        <a id="i3pu16" style={{
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
        <a id="i6504e" style={{
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
        <a id="i53lcl" style={{
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
        <a id="i3lbae" style={{
            "padding": "8px 16px",
            "fontSize": "0.9rem",
            "fontWeight": "600",
            "textDecoration": "none",
            "transition": "all 0.2s",
            "background": "rgba(85, 70, 217, 0.1)",
            "color": "#5546d9",
            "borderRadius": "16px",
            "--chart-color-palette": "default"
          }} onClick={(e) => { if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; e.preventDefault(); navigate("/categories-profile"); }} href="/categories-profile" {...{"data-navigate-to": "categories-profile"}}>{"Categories & Profile"}</a>
      </div>
    </nav>
    <main id="iuwb1w" className="assistant-main" style={{"padding": "24px 16px", "margin": "0 auto", "maxWidth": "1200px", "--chart-color-palette": "default"}}>
      <header id="container_header_5" className="app-head">
        <div id="Component_35">
          <p id="p_21" className="app-eyebrow">{"MAKE IT YOURS"}</p>
          <h1 id="h1_5">{"Your space, organized."}</h1>
          <p id="p_22">{"Keep your goal categories and account details together."}</p>
        </div>
        <div id="a_10" className="app-link" {...{"href": "/dashboard"}}>{"Back to overview"}</div>
      </header>
      <section id="container_section_16" className="app-wrap">
        <h2 id="h2_15" className="app-section-title">{"Categories"}</h2>
        <p id="p_23" className="app-section-sub">{"Organize resolutions with names and colors that make sense to you."}</p>
        <div id="Component_36" className="app-panel app-table">
          <TableBlock id="table-category-categories-profile" styles={{"width": "100%", "margin": "12px 0", "minHeight": "300px", "borderRadius": "12px", "--chart-color-palette": "default"}} title="Goal categories and colors" options={{
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
                  "label": "Color hex",
                  "column_type": "field",
                  "field": "colorHex",
                  "type": "str",
                  "required": true
                },
                {
                  "label": "Created at",
                  "column_type": "field",
                  "field": "createdAt",
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
                  "field": "colorHex",
                  "label": "colorHex",
                  "type": "str",
                  "required": false,
                  "defaultValue": null
                },
                {
                  "column_type": "lookup",
                  "path": "resolutions",
                  "field": "resolutions",
                  "lookup_field": "title",
                  "target_field": "id",
                  "target_type": "int",
                  "entity": "Resolution",
                  "type": "list",
                  "required": false
                }
              ]
            }} dataBinding={{"entity": "Category", "endpoint": "/category/", "row_key_fields": ["id"]}} />
        </div>
        <div id="Component_37" className="app-actions">
          <CrudButton id="action_button_15" className="action-button-component" label="Add CategoryAdd Category" action="create" tableId="table-category-categories-profile" entity="Category" />
          <CrudButton id="action_button_16" className="action-button-component" label="Edit CategoryEdit Category" action="update" tableId="table-category-categories-profile" entity="Category" />
          <CrudButton id="action_button_17" className="action-button-component" label="Delete CategoryDelete Category" action="delete" tableId="table-category-categories-profile" entity="Category" confirmMessage="Delete the selected category?" />
        </div>
      </section>
      <section id="container_section_17" className="app-wrap">
        <h2 id="h2_16" className="app-section-title">{"Profile"}</h2>
        <p id="p_24" className="app-section-sub">{"Your account information and access history."}</p>
        <div id="Component_38" className="app-panel app-table">
          <TableBlock id="table-user-categories-profile" styles={{"width": "100%", "margin": "12px 0", "minHeight": "300px", "borderRadius": "12px", "--chart-color-palette": "default"}} title="Your profile details" options={{
              "showHeader": true,
              "stripedRows": false,
              "showPagination": true,
              "rowsPerPage": 5,
              "actionButtons": true,
              "columns": [
                {
                  "label": "Full name",
                  "column_type": "field",
                  "field": "fullName",
                  "type": "str",
                  "required": true
                },
                {
                  "label": "Email",
                  "column_type": "field",
                  "field": "email",
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
                  "label": "Last login at",
                  "column_type": "field",
                  "field": "lastLoginAt",
                  "type": "datetime",
                  "required": true
                }
              ],
              "formColumns": [
                {
                  "column_type": "field",
                  "field": "fullName",
                  "label": "fullName",
                  "type": "str",
                  "required": true,
                  "defaultValue": null
                },
                {
                  "column_type": "field",
                  "field": "email",
                  "label": "email",
                  "type": "str",
                  "required": true,
                  "defaultValue": null
                },
                {
                  "column_type": "field",
                  "field": "lastLoginAt",
                  "label": "lastLoginAt",
                  "type": "datetime",
                  "required": false,
                  "defaultValue": null
                },
                {
                  "column_type": "lookup",
                  "path": "resolutions",
                  "field": "resolutions",
                  "lookup_field": "title",
                  "target_field": "id",
                  "target_type": "int",
                  "entity": "Resolution",
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
                  "path": "habits",
                  "field": "habits",
                  "lookup_field": "name",
                  "target_field": "id",
                  "target_type": "int",
                  "entity": "Habit",
                  "type": "list",
                  "required": false
                }
              ]
            }} dataBinding={{"entity": "User", "endpoint": "/user/", "row_key_fields": ["id"]}} />
          <div id="ixvkz3" className="assistant-method-buttons" style={{"margin": "16px 0", "display": "flex", "--chart-color-palette": "default", "flexWrap": "wrap", "gap": "8px"}}>
            <MethodButton id="iu3pma" className="action-button-component" style={{
                "padding": "6px 14px",
                "margin": "4px",
                "fontSize": "13px",
                "fontWeight": "600",
                "display": "flex",
                "cursor": "pointer",
                "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)",
                "color": "#fff",
                "borderRadius": "4px",
                "border": "none",
                "--chart-color-palette": "default",
                "alignItems": "center"
              }} endpoint="/user/{user_id}/methods/createResolution/" label="createResolutioncreateResolution" parameters={[{"name": "title", "type": "str", "required": true}, {"name": "description", "type": "str", "required": true}]} isInstanceMethod={true} instanceSourceTableId="table-user-categories-profile" />
            <MethodButton id="ivcc6s" className="action-button-component" style={{
                "padding": "6px 14px",
                "margin": "4px",
                "fontSize": "13px",
                "fontWeight": "600",
                "display": "flex",
                "cursor": "pointer",
                "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)",
                "color": "#fff",
                "borderRadius": "4px",
                "border": "none",
                "--chart-color-palette": "default",
                "alignItems": "center"
              }} endpoint="/user/{user_id}/methods/addProgressEntry/" label="addProgressEntryaddProgressEntry" parameters={[
                {
                  "name": "resolution",
                  "type": "Resolution",
                  "required": true,
                  "inputKind": "lookup",
                  "entity": "Resolution",
                  "lookupField": "title"
                },
                {
                  "name": "entry",
                  "type": "ProgressEntry",
                  "required": true,
                  "inputKind": "lookup",
                  "entity": "ProgressEntry",
                  "lookupField": "date"
                }
              ]} isInstanceMethod={true} instanceSourceTableId="table-user-categories-profile" />
          </div>
        </div>
      </section>
    </main>    </div>
  );
};

export default CategoriesProfile;
