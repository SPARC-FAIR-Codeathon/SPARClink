import { Entry } from "contentful";
import {ExtendedVue, Vue, VueConfiguration, VueConstructor} from "vue/types/vue";

interface Tag {
  name: string;
  slug: string
}

/**
 *
 * this utility type is provided by contentful, and demonstrates basic generics:
 *
 * export interface Entry<T> {
 *   sys: Sys;
 *   fields: T;
 *   toPlainObject(): object;
 *   update(): Promise<Entry<T>>;
 * }
 *
 * in english: "take the type argument: T, and make that the fields key in the object"
 *
 * the result:
 * {
 *   sys: Sys;
 *   fields: Tag
 * }
 */
type TagEntry = Entry<Tag>

interface Filter {
  category: string
  tags?: TagEntry[]
}

interface TransformedInnerFilter {
  label: string;
  category: string;
  key: string
  value: boolean;
}

type TransformedFilter = Filter & {
  filters: TransformedInnerFilter[]
}

/**
 * this is the type signature for the function below.  It takes a Filter, and returns a TransformedFilter
 */
type FilterTransform = (filter: Filter) => TransformedFilter

/**
 * since you know the shape of the thing you are dealing with, and the shape of the thing you want to return,
 * you end up with a function that is much easier to read and understand, IMHO
 */
export const transformIndividualFilter: FilterTransform = outerFilter => ({
  ...outerFilter,
  filters: (outerFilter.tags ?? []).map(t => ({
    label: t.fields.name,
    category: outerFilter.category,
    key: t.fields.slug,
    value: false
  }))
})


interface OuterFilter {
  type: string;
  filters?: Entry<Filter>[]
}

/**
 * here we see the generics at work again.  We're able to concisely express
 * the complicated nesting of { sys, fields } objects that occurs when we
 * model things in contentful
 */
type FilterResponse = Entry<OuterFilter>

type TransformFilters = (fields: FilterResponse['fields']) => TransformedFilter[]

/**
 * and now the function is much more readable
 * the type system made it immediately apparent that the original function's 'flatten' operation
 * was actually an unnecessary no-op
 */
export const transformFilters: TransformFilters = fields =>
  (fields.filters ?? [])
    .map(f => transformIndividualFilter(f.fields))

/**
 * common function to bubble the search change event from a component containing an el-table to a parent component
 */
export const onSortChange = (instance: Vue<{}>, payload: SortChangeEvent): void => {
  instance.$emit('sort-change', payload)
}

interface SearchData {
  limit: number;
  skip: number;
  items: unknown[];
  order?: string
  ascending: boolean;
}

interface SortChangeEvent {
  column: unknown;
  prop: string;
  order: 'ascending' | 'descending' | null
}

/**
 * mutates the searchData parameter according to the payload parameter
 * calls the passed fetchResults function to get new, sorted results
 * @param dataSource indicates which API we are using
 * @param searchData gets mutated based on payload
 * @param fetchResults called once searchData is updated
 * @param payload the sort event
 */
export const handleSortChange = (
  dataSource: 'contentful' | 'blackfynn',
  searchData: SearchData,
  fetchResults: () => void,
  payload: SortChangeEvent
): void => {
  searchData.skip = 0
  if (dataSource === 'blackfynn') {
    searchData.order = payload.order === null || payload.prop === 'createdAt'
      ? 'date'
      : payload.prop
    searchData.ascending = payload.order === 'ascending'
  } else {
    searchData.order = payload.order === null
      ? undefined
      : `${payload.order === 'descending' ? '-' : ''}${payload.prop}`
  }

  fetchResults()
}

/**
 * Gets the file extension for a file or path
 * @param path Path or filename
 * @returns String containing the file extension
 */
export const extractExtension = (
  path : string
): string => {
  const split = path.split('.')
  if (split.length > 1) {
    const ext = split.pop()
    return ext || ''
  }
  return ''
}
