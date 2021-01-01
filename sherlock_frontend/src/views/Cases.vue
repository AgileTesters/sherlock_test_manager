<template>
  <navBar />

  <div class="tile is-ancestor" style="margin-top:30px; width:95%; margin:auto">
    <div class="tile is-5 is-vertical is-parent">
      <div
        class="tile is-child box sherlock_tiles has-text-right"
        style="max-height: 100px;"
      >
        <div class="has-text-left" v-if="project">
          <p style="font-size: 7px;">
            project name:
          </p>
          <p style="font-size: 27px; font-weight: 600">
            {{ project.name }}
          </p>
        </div>
      </div>
      <div
        class="tile is-child box sherlock_tiles has-text-right"
        style="max-height: 250px;"
      >
        <p class="has-text-left" style="font-size: 7px;">
          new case:
        </p>
        <br />
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
        <a class="button" @click="addNewCase">save case</a>
      </div>

      <div class="tile is-child">
        <div class="tile is-parent">
          <div class="tile is-1 is-child"></div>

          <div class="tile is-child box is-4 sherlock_tiles has-text-centered">
            <i class="fab fa-markdown" style="font-size:50px"></i>
            <p class="has-text-left is-size-7">
              Sherlock support <b>#Markdown</b> language! <br />
              Click
              <a href="https://www.markdownguide.org/basic-syntax/"> here </a>
              to find out more about the syntax
            </p>
          </div>

          <div class="tile is-2 is-child"></div>

          <div class="tile is-child box is-4 sherlock_tiles has-text-centered">
            <i class="fal fa-keyboard" style="font-size:50px"></i>
            <p class="has-text-left is-size-7">
              Press SHIFT + ENTER to save your new test case
            </p>
          </div>
          <div class="tile is-1 is-child"></div>
        </div>
      </div>
    </div>

    <div class="tile is-parent is-vertical">
      <div class="tile is-child box case_tile">
        <table class="table is-fullwidth" v-if="cases.length > 0">
          <thead>
            <tr>
              <th class="col_id">
                <input type="checkbox" />
              </th>
              <th></th>
              <th>
                <span>
                  cases
                </span>
              </th>
              <th style="text-align: right;">
                <span>
                  <attachModal
                    v-bind:casesSelected="casesSelected"
                    v-bind:cases="cases"
                    v-bind:projectId="projectId"
                  />
                </span>
              </th>
            </tr>
          </thead>
          <tbody v-for="item in cases" :key="item.exhibition_order">
            <tr>
              <td class="col_id">
                <input type="checkbox" :value="item" v-model="casesSelected" />
              </td>
              <td class="col_id">
                <span>{{ item.order_index }}</span>
              </td>
              <td>
                <VueMarkdownIt
                  class="content"
                  :source="item.name"
                  v-bind:typographer="true"
                  v-bind:breaks="true"
                  v-bind:html="true"
                  :plugins="plugins"
                />
              </td>
              <td style="text-align: right;"><caseMenuElipisis /></td>
            </tr>
            <tr
              v-for="sub_item in item.child_cases"
              :key="sub_item.exhibition_order"
            >
              <td class="col_id">
                <input
                  type="checkbox"
                  :value="sub_item"
                  v-model="casesSelected"
                />
              </td>
              <td class="col_id">
                <span>{{ item.order_index }}</span
                >-<span>{{ sub_item.exhibition_order }}</span>
              </td>
              <td>
                <div class="columns">
                  <div class="column is-1"></div>
                  <div class="column">
                    <VueMarkdownIt
                      class="content"
                      v-bind:typographer="true"
                      :source="sub_item.name"
                      v-bind:breaks="true"
                      v-bind:html="true"
                      :plugins="plugins"
                    />
                  </div>
                </div>
              </td>
              <td style="text-align: right !important;">
                <caseMenuElipisis />
              </td>
            </tr>
          </tbody>
        </table>
        <!-- <nav
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
        </nav> -->
        <div v-else class="has-text-centered" style="margin">
          <i class="fal fa-cat-space" style="font-size:50px"></i><br />
          <p class="is-family-monospace	is-size-7">
            So much empty space....
          </p>
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
      project: null,
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
          console.log(this.cases);
        })
        .catch(error => {
          this.error = error;
        });
    },
    fetchProjectDetails() {
      var requestOptions = {
        method: "get",
        url: "/projects/project/" + this.projectId
      };
      axios(requestOptions)
        .then(response => {
          this.project = response.data;
        })
        .catch(error => {
          this.error = error;
        });
    }
  },
  async mounted() {
    await this.fetchCases();
    await this.fetchProjectDetails();
  }
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
