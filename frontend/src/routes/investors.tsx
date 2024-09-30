import {
	Table,
	TableBody,
	TableCaption,
	TableCell,
	TableFooter,
	TableHead,
	TableHeader,
	TableRow,
} from "@/components/ui/table";
import { useQuery } from "@tanstack/react-query";
import { investors } from "@/api.ts";

function formatBigInt(number: number): string {
	if (number > 1_000_000_000) {
		return `${(number / 1_000_000_000).toFixed(1)}B`;
	}
	return `${number}`;
}

function InvestorsTable() {
	const {
		isPending,
		error,
		data: paginatedResponse,
	} = useQuery({
		queryKey: ["investors"],
		queryFn: investors,
	});
	if (isPending) {
		return <>Loading...</>;
	}

	if (error) return `An error has occurred: ${error.message}`;
	const total = paginatedResponse.data.reduce(
		(acc, cur) => acc + cur.totalCommitment,
		0,
	);
	return (
		<Table>
			<TableCaption>List of all investors.</TableCaption>
			<TableHeader>
				<TableRow>
					<TableHead className="w-[100px]">id</TableHead>
					<TableHead>Name</TableHead>
					<TableHead>Type</TableHead>
					<TableHead>Date Added</TableHead>
					<TableHead>City</TableHead>
					<TableHead className="text-right">Amount</TableHead>
				</TableRow>
			</TableHeader>
			<TableBody>
				{paginatedResponse.data.map((investor) => (
					<TableRow key={investor.id}>
						<TableCell className="font-medium">{investor.id}</TableCell>
						<TableCell>{investor.name}</TableCell>
						<TableCell>{investor.type}</TableCell>
						<TableCell>{investor.dateAdded.toDateString()}</TableCell>
						<TableCell>{investor.address}</TableCell>
						<TableCell className="text-right">
							{formatBigInt(investor.totalCommitment)}
						</TableCell>
					</TableRow>
				))}
			</TableBody>
			<TableFooter>
				<TableRow>
					<TableCell colSpan={5}>Total</TableCell>
					<TableCell className="text-right">{formatBigInt(total)}</TableCell>
				</TableRow>
			</TableFooter>
		</Table>
	);
}

function Investors() {
	return (
		<>
			<h2 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl mb-3">
				Investors
			</h2>
			<InvestorsTable />
		</>
	);
}

export default Investors;
