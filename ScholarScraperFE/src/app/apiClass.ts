export class Scholar {
    fullname: string;
    id: string;
    parse: boolean
}

export class Publication {
    citation_count: number;
    date: string;
    id: string;
    title: string;
}


export class PublicationAuthor {
    publicationID: string;
    scholarID: string;
}

export class PublicationCites {
    publication1: string;
    publication2: string;
}

export class TotalCites {
    date: string;
    scholar_id: string;
    total_cites: number; 
}