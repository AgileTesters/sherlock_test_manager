import { createRouter, createWebHistory } from "vue-router";
import Index from "../views/Index.vue";
import Dashboard from "../views/Dashboard.vue";
import ProjectDashboard from "../views/ProjectDashboard.vue";
import ManageCases from "../views/Cases.vue";
import ExecuteCase from "../views/CaseExecution.vue";

const routes = [
  {
    path: "/login",
    name: "Index",
    component: Index
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: Dashboard
  },
  {
    path: "/project/:projectId/dashboard",
    name: "projectDashboard",
    component: ProjectDashboard
  },
  {
    path: "/project/:projectId/cases",
    name: "manageCases",
    component: ManageCases
  },
  {
    path: "/project/:projectId/execute",
    name: "executeCases",
    component: ExecuteCase
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
