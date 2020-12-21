<template>
  <navBar />

  <div class="tile is-ancestor" style="margin-top:30px; width:95%; margin:auto">
    <div class="tile is-5 is-vertical is-parent">
      <div class="tile is-child box sherlock_tiles">
        <div class="field">
          <div class="control">
            <textarea
              class="textarea is-default"
              placeholder="press shift + enter to save your case"
              v-model="newCase"
              @keyup.shift.enter="addNewCase"
            ></textarea>
          </div>
        </div>
      </div>
    </div>
    <div class="tile is-parent">
      <div class="tile is-child box case_tile">
        <table class="table is-fullwidth" v-if="cases.length > 0">
          <thead>
            <tr>
              <th></th>
              <th>ref</th>
              <th colspan="2">
                <span>
                  cases
                </span>
                <span>
                  <attachModal
                    v-bind:casesSelected=casesSelected
                    v-bind:cases=cases
                    v-bind:projectId=projectId
                  />
                </span>
              </th>
            </tr>
          </thead>
          <tbody v-for="item in cases" :key="item.id">
            <tr>
              <th>
                <input
                  type="checkbox"
                  :value="item"
                  v-model="casesSelected"
                />
              </th>
              <th class="col_id">
                <span>{{ item.id }}</span>
              </th>
              <td><VueMarkdownIt :source="item.name" /></td>
              <td><caseMenuElipisis /></td>
            </tr>
            <tr v-for="sub_item in item.child_cases" :key="sub_item.id">
              <th>
                <input
                  type="checkbox"
                  :value="sub_item"
                  v-model="casesSelected"
                />
              </th>
              <th class="col_id">
                <span>{{ item.id }}</span
                >-<span>{{ sub_item.id }}</span>
              </th>
              <td>
                <div class="columns">
                  <div class="column is-1"></div>
                  <div class="column">
                    <VueMarkdownIt :source="sub_item.name" />
                  </div>
                </div>
              </td>
              <td><caseMenuElipisis /></td>
            </tr>
          </tbody>
        </table>
        <nav
          class="pagination is-small"
          role="navigation"
          aria-label="pagination"
          v-if="cases.length > 0"
        >
          <a class="pagination-previous">Previous</a>
          <a class="pagination-next">Next page</a>



          <ul class="pagination-list">
            <li><a class="pagination-link" aria-label="Goto page 1">1</a></li>
            <li><span class="pagination-ellipsis">&hellip;</span></li>
            <li><a class="pagination-link" aria-label="Goto page 45">45</a></li>
            <li>
              <a
                class="pagination-link is-current"
                aria-label="Page 46"
                aria-current="page"
                >46</a
              >
            </li>
            <li><a class="pagination-link" aria-label="Goto page 47">47</a></li>
            <li><span class="pagination-ellipsis">&hellip;</span></li>
            <li><a class="pagination-link" aria-label="Goto page 86">86</a></li>
          </ul>
        </nav>
        <div v-else>
          No case created yet :)
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import NavBar from "@/components/InternalNavBar";
import CaseMenuElipisis from "@/components/Cases/CaseElipsisMenu";
import AttachModal from "@/components/Cases/AttachModal";

import VueMarkdownIt from "vue3-markdown-it";
import MarkdownHighligh from "markdown-it-highlightjs";

export default {
  components: {
    VueMarkdownIt,
    navBar: NavBar,
    caseMenuElipisis: CaseMenuElipisis,
    attachModal: AttachModal
  },
  data() {
    return {
      projectId: this.$route.params.projectId,
      cases: [],
      casesSelected: [],
      newCase: "",
      loading: false,
      tag_field: "",
      error: null,
      showAttachCasesModal: false,
      plugins: [
        {
          plugin: MarkdownHighligh
        }
      ]
    };
  },
  methods: {
    addNewCase() {
      if (this.newCase === "") {
        console.log("blank test case");
      } else {
        const payload = {
          test_case_text: this.newCase,
          project_id: this.projectId,
          parent_id: "0"
        };
        const requestOptions = {
          method: "post",
          url: "/cases/new",
          data: payload
        };
        axios(requestOptions)
          .then(response => {
            // TODO: add visual feedback that is working
            if (response.data.message != "CASE_CREATED") {
              this.error = response.data.message;
            } else {
              this.fetchCases();
              this.newCase = "";
            }
          })
          .catch(error => {
            this.error = error;
          });
      }
    },
    fetchCases() {
      var requestOptions = {
        method: "get",
        url: "/cases/find_by_project/" + this.projectId
      };
      axios(requestOptions)
        .then(response => {
          this.cases = response.data;
        })
        .catch(error => {
          this.error = error;
        });
    }
  },
  async mounted() {
    await this.fetchCases();
  },
};
</script>
<style>
.child_cases {
  background-color: #eff1f3;
}

.col_id {
  vertical-align: middle !important;
  font-size: 09px;
  width: 60px;
}
</style>
