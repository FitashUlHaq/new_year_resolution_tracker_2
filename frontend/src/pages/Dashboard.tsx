import React from "react";
import { useNavigate } from "react-router-dom";
import { ChartBlock } from "../components/runtime/ChartBlock";
import { TableBlock } from "../components/runtime/TableBlock";
import { MetricCardBlock } from "../components/runtime/MetricCardBlock";
import { MethodButton } from "../components/MethodButton";

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  return (
    <div id="page-dashboard" style={{
              "fontFamily": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
              "minHeight": "100vh",
              "background": "#f7f6fb",
              "color": "#23213a",
              "--chart-color-palette": "default"
            }}>
    <nav id="iwpp" className="assistant-nav-header" style={{
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
      <p id="ifaa" style={{"fontSize": "1.25rem", "fontWeight": "700", "letterSpacing": "-0.01em", "color": "#23213a", "--chart-color-palette": "default"}}>{"Stride"}</p>
      <div id="iisl" style={{"display": "flex", "--chart-color-palette": "default", "alignItems": "center", "gap": "4px"}}>
        <a id="ivu8" style={{
            "padding": "8px 16px",
            "fontSize": "0.9rem",
            "fontWeight": "600",
            "textDecoration": "none",
            "transition": "all 0.2s",
            "background": "rgba(85, 70, 217, 0.1)",
            "color": "#5546d9",
            "borderRadius": "16px",
            "--chart-color-palette": "default"
          }} onClick={(e) => { if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; e.preventDefault(); navigate("/dashboard"); }} href="/dashboard" {...{"data-navigate-to": "dashboard"}}>{"Dashboard"}</a>
        <a id="i39yh" style={{
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
        <a id="i2dvl" style={{
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
        <a id="i2j35" style={{
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
        <a id="i9i9g" style={{
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
    <main id="iqwy5" className="assistant-main" style={{"padding": "24px 16px", "margin": "0 auto", "maxWidth": "1200px", "--chart-color-palette": "default"}}>
      <header id="container_header" className="app-head">
        <div id="Component">
          <p id="p" className="app-eyebrow">{"YOUR SPACE TO GROW"}</p>
          <h1 id="h1">{"Make the next step count."}</h1>
          <p id="p_2">{"See your goals, keep your habits close, and make progress visible."}</p>
        </div>
        <div id="a" className="ds-btn ds-btn-primary" {...{"href": "/resolutions"}}>{"Manage resolutions"}</div>
      </header>
      <section id="container_section" className="app-band">
        <div id="Component_2">
          <h2 id="h2">{"Momentum starts here"}</h2>
          <p id="p_3">{"Make room for the small actions that move your bigger goals forward."}</p>
        </div>
        <div id="a_2" {...{"href": "/habits"}}>{"Check your habits →"}</div>
      </section>
      <section id="container_section_2" className="app-wrap">
        <h2 id="h2_2" className="app-section-title">{"Your overview"}</h2>
        <p id="p_4" className="app-section-sub">{"A live snapshot of your goals and routines."}</p>
        <div id="Component_3" className="app-panel">
          <MetricCardBlock id="i3yma" className="metric-card-component" styles={{"width": "100%", "margin": "8px 0", "minHeight": "140px", "--chart-color-palette": "default"}} metric={{
              "metricTitle": "Total resolutions",
              "format": "number",
              "valueColor": "#2c3e50",
              "valueSize": 32,
              "showTrend": true,
              "positiveColor": "#27ae60",
              "negativeColor": "#e74c3c",
              "value": 0,
              "trend": 12
            }} dataBinding={{"entity": "Resolution", "endpoint": "/resolution/", "row_key_fields": ["id"], "aggregation": "count"}} />
        </div>
      </section>
      <section id="container_section_3" className="app-wrap">
        <h2 id="h2_3" className="app-section-title">{"Goals in motion"}</h2>
        <div id="Component_4" className="app-panel">
          <MetricCardBlock id="iax6v" className="metric-card-component" styles={{"width": "100%", "margin": "8px 0", "minHeight": "140px", "--chart-color-palette": "default"}} metric={{
              "metricTitle": "Active resolutions",
              "format": "number",
              "valueColor": "#2c3e50",
              "valueSize": 32,
              "showTrend": true,
              "positiveColor": "#27ae60",
              "negativeColor": "#e74c3c",
              "value": 0,
              "trend": 12
            }} dataBinding={{"entity": "Resolution", "endpoint": "/resolution/", "row_key_fields": ["id"], "filter_expression": "status == ACTIVE", "aggregation": "count"}} />
        </div>
      </section>
      <section id="container_section_4" className="app-wrap">
        <h2 id="h2_4" className="app-section-title">{"Habit momentum"}</h2>
        <div id="Component_5" className="app-panel">
          <MetricCardBlock id="icvsf" className="metric-card-component" styles={{"width": "100%", "margin": "8px 0", "minHeight": "140px", "--chart-color-palette": "default"}} metric={{
              "metricTitle": "Average habit streak",
              "format": "number",
              "valueColor": "#2c3e50",
              "valueSize": 32,
              "showTrend": true,
              "positiveColor": "#27ae60",
              "negativeColor": "#e74c3c",
              "value": 0,
              "trend": 12
            }} dataBinding={{"entity": "Habit", "endpoint": "/habit/", "row_key_fields": ["id"], "data_field": "currentStreak", "aggregation": "average"}} />
        </div>
      </section>
      <section id="container_section_5" className="app-wrap">
        <p id="p_5" className="app-section-sub">{"See how your goals are distributed across each stage."}</p>
        <div id="Component_6" className="app-panel">
          <ChartBlock id="iiro4" className="pie-chart-component" styles={{"width": "100%", "margin": "12px 0", "minHeight": "400px", "borderRadius": "12px", "--chart-color-palette": "default"}} chartType="pie-chart" title="Resolutions by status" color="default" chart={{
              "showLegend": true,
              "legendPosition": "bottom",
              "showLabels": true,
              "labelPosition": "inside",
              "paddingAngle": 0,
              "innerRadius": 0,
              "outerRadius": 80,
              "startAngle": 0,
              "endAngle": 360
            }} series={[
              {
                "name": "Resolution",
                "label": "Resolution",
                "color": "#00C49F",
                "dataSource": "resolution",
                "endpoint": "/resolution/",
                "labelField": "status",
                "aggregation": "count"
              }
            ]} dataBinding={{"entity": "Resolution", "endpoint": "/resolution/", "row_key_fields": ["id"], "label_field": "status", "aggregation": "count"}} />
        </div>
      </section>
      <section id="container_section_6" className="app-wrap">
        <h2 id="h2_5" className="app-section-title">{"Progress journal"}</h2>
        <p id="p_6" className="app-section-sub">{"Your recorded actions, notes, and amounts in one place."}</p>
        <div id="Component_7" className="app-panel app-table">
          <TableBlock id="table-progressentry-dashboard" styles={{"width": "100%", "margin": "12px 0", "minHeight": "300px", "borderRadius": "12px", "--chart-color-palette": "default"}} title="Progress journal entries" options={{
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
          <div id="iz006" className="assistant-method-buttons" style={{"margin": "16px 0", "display": "flex", "--chart-color-palette": "default", "flexWrap": "wrap", "gap": "8px"}}>
            <MethodButton id="imv0t" className="action-button-component" style={{
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
              }} endpoint="/progressentry/{progressentry_id}/methods/edit/" label="editedit" parameters={[{"name": "notes", "type": "str", "required": true}, {"name": "amount", "type": "float", "required": true}]} isInstanceMethod={true} instanceSourceTableId="table-progressentry-dashboard" />
            <MethodButton id="igt9d" className="action-button-component" style={{
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
              }} endpoint="/progressentry/{progressentry_id}/methods/remove/" label="removeremove" isInstanceMethod={true} instanceSourceTableId="table-progressentry-dashboard" />
          </div>
        </div>
        <div id="Component_8" className="app-actions">
          <div id="a_3" {...{"href": "/resolution-detail"}}>{"Explore a resolution"}</div>
        </div>
      </section>
    </main>    </div>
  );
};

export default Dashboard;
