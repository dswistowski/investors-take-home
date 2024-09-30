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

interface AssetClass {
	id: number;
	name: string;
	value: number;
}

interface ApiCommitment {
	id: number;
	asset_class: string;
	currency: string;
	amount: number;
}

interface Commitment {
	id: number;
	assetClass: string;
	currency: string;
	amount: number;
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

export const assetClass = (investorId: number) => async () => {
	const url = `${config.backendApiUrl}/investors/${investorId}/asset-classes/`;
	const response = await fetch(url);
	return (await response.json()) as Array<AssetClass>;
};

export const commitments =
	(investorId: number, assetClass: number | undefined) =>
	async (): Promise<PaginatedResponse<Commitment>> => {
		const url =
			assetClass === undefined
				? `${config.backendApiUrl}/investors/${investorId}/commitment/`
				: `${config.backendApiUrl}/investors/${investorId}/commitment/?asset_class_id=${assetClass}`;
		const response = await fetch(url);
		const paginatedResponse =
			(await response.json()) as PaginatedResponse<ApiCommitment>;

		return {
			...paginatedResponse,
			data: paginatedResponse.data.map((api) => ({
				...api,
				assetClass: api.asset_class,
			})),
		};
	};
