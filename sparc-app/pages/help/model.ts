import {Entry} from "contentful";

export type HelpDocument = Entry<{
  title?: string;
  summary?: string;
  helpContent?: string;
  tags?: string[]
}>


export type HelpSection = Entry<{
  title: string;
  helpDocuments: HelpDocument[]
}>

export interface HelpData {
  title: string;
  summary: string;
  sections: HelpSection[]
}

export interface Data {
  allHelpData: Partial<HelpData>
  helpData: Partial<HelpData>;
  isLoadingSearch: boolean;
  searchTerms?: string;
}

export interface Methods {
  doSearch: (terms: string | undefined) => void
}