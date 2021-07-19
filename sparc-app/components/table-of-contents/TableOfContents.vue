<template>
  <div class="table-of-contents">
    <ul>
      <li v-for="element in elements" :key="element.href">
        <a href="element.anchor">{{ element.title }}</a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'TableOfContents',
  data: () => ({
    elements: [
      {
        title: 'Properties',
        href: '#properties'
      },
      {
        title: 'Section 1',
        href: '#section1'
      },
      {
        title: 'Section 2',
        href: '#section2'
      }
    ]
  })
}
</script>

<style lang="scss" scoped>
.table-of-contents {
  ul {
    padding: 0;
    margin: 0;

    list-style-type: none;
    li {
      display: inline;

      a {
        text-decoration: none;
        color: black;

        &:hover {
          text-decoration: underline;
        }

        &.active {
          color: #8300bf;
          font-weight: bold;
        }
      }
    }

    li:after {
      padding: 0 1em;
      content: '\00b7';
      font-weight: bold;
    }

    li:last-child:after {
      content: none;
    }
  }
}
</style>
