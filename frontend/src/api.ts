import { config } from "@/config.ts";

interface Investor {
	id: number;
	name: string;
	type: string;
	dateAdded: Date;
	address: string;
	totalCommitment: number;
}

interface ApiInvestor {
	id: number;
	name: string;
	type: string;
	date_added: string;
	address: string;
	total_commitment: number;
}

interface PaginatedResponse<T> {
	data: Array<T>;
	paging: {
		next: string | null;
		previous: string | null;
	};
}

export async function investors(): Promise<PaginatedResponse<Investor>> {
	const url = `${config.backendApiUrl}/investors/`;

	const response = await fetch(url);
	const paginatedResponse: PaginatedResponse<ApiInvestor> =
		await response.json();
	return {
		...paginatedResponse,
		data: paginatedResponse.data.map((api) => ({
			...api,
			dateAdded: new Date(api.date_added),
			totalCommitment: api.total_commitment,
		})),
	};
}
