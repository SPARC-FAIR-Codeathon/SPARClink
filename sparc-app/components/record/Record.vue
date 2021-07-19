<template>
  <div class="sparc-record">
    <div class="header">
      <div class="gradient">
        <el-row type="flex" justify="center">
          <el-col :xs="22" :sm="22" :md="22" :lg="18" :xl="16">
            <div class="breadcrumb">
              <span class="segment">
                <a href="#">Data Core</a>
              </span>
              <span class="divider">/</span>
              <span class="segment">
                <a href="#">{{ title }}</a>
              </span>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
    <div class="page">
      <el-row type="flex" justify="center">
        <el-col :xs="22" :sm="22" :md="22" :lg="18" :xl="16">
          <div class="section">
            <h1>{{ title }}</h1>
          </div>
          <div class="section table-of-contents">
            <table-of-contents />
          </div>
          <div class="section properties">
            <h3>Properties</h3>
            <el-table :show-header="false" :data="properties">
              <el-table-column prop="key" width="120" />
              <el-table-column prop="value" width="120" />
            </el-table>
          </div>
          <div v-for="section in sections" :key="section.key" class="section">
            <h3>{{ section.title }}</h3>
            <data-table table-class="record-section-table" />
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import DataTable from '../data-table/DataTable.vue'
import TableOfContents from '../table-of-contents/TableOfContents.vue'

export default {
  name: 'SparcRecord',
  components: {
    DataTable,
    TableOfContents
  },
  data: () => ({
    title: 'Record Title',
    properties: [
      {
        key: 'Key 1',
        value: 'Value 1'
      },
      {
        key: 'Key 2',
        value: 'Value 2'
      }
    ],
    sections: [
      {
        key: 'section1',
        title: 'Section 1',
        data: []
      },
      {
        key: 'section2',
        title: 'Section 2',
        data: []
      }
    ]
  })
}
</script>

<style lang="scss">
.record-section-table {
  border-radius: 5px;
}
</style>

<style lang="scss" scoped>
.header {
  .gradient {
    padding: 1.5em 0;
    color: #f0f2f5;
    background-image: linear-gradient(90deg, #0026ff 0%, #00ffb9 100%);
  }
}

.page {
  padding-top: 2em;
}

.breadcrumb {
  .segment {
    a {
      text-decoration: none;
      color: white;
    }
  }

  .divider {
    padding: 0 0.5em;
  }
}

.section {
  padding: 1em 0;

  h3 {
    margin-bottom: 0.5em;
  }
}
</style>
