import { useQuery } from "@tanstack/react-query";
import { assetClass as getAssetClass, commitments } from "@/api.ts";
import { useParams, Navigate } from "react-router-dom";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group.tsx";
import { Label } from "@/components/ui/label.tsx";
import { formatBigInt } from "@/numbers.ts";
import { useState } from "react";
import {
	Table,
	TableBody,
	TableCaption,
	TableCell,
	TableFooter,
	TableHead,
	TableHeader,
	TableRow,
} from "@/components/ui/table.tsx";

function AssetClassSelector({
	investorId,
	assetClass: selectedAssetClass,
	setAssetClass,
}: {
	investorId: number;
	assetClass?: number;
	setAssetClass: (assetClass?: number) => void;
}) {
	const {
		isPending,
		error,
		data: assetClasses,
	} = useQuery({
		queryKey: ["asset-class-selector", investorId],
		queryFn: getAssetClass(investorId),
	});
	if (isPending) return <>Loading...</>;
	if (error) return `An error has occurred: ${error.message}`;

	const total = assetClasses.reduce(
		(acc, assetClass) => acc + assetClass.value,
		0,
	);

	return (
		<RadioGroup defaultValue="all" className="flex flex-wrap mt-3 gap-4">
			<div>
				<RadioGroupItem
					value="all"
					id="all"
					className="peer sr-only"
					aria-label="Card"
					onClick={() => setAssetClass(undefined)}
					checked={selectedAssetClass === undefined}
				/>
				<Label
					htmlFor="all"
					className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-transparent p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
				>
					<div className="text-xl">All</div>
					<div>{formatBigInt(total)}</div>
				</Label>
			</div>
			{assetClasses.map((assetClass) => (
				<div key={assetClass.id}>
					<RadioGroupItem
						value={assetClass.id.toString()}
						id={assetClass.id.toString()}
						className="peer sr-only"
						aria-label={assetClass.name}
						onClick={() => setAssetClass(assetClass.id)}
						checked={selectedAssetClass === assetClass.id}
					/>
					<Label
						htmlFor={assetClass.id.toString()}
						className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-transparent p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
					>
						<div className="text-xl">{assetClass.name}</div>
						<div>{formatBigInt(assetClass.value)}</div>
					</Label>
				</div>
			))}
		</RadioGroup>
	);
}

function CommitmentsTable({
	investorId,
	assetClass,
}: { investorId: number; assetClass: number | undefined }) {
	const {
		isPending,
		error,
		data: paginatedResponse,
	} = useQuery({
		queryKey: ["commitment", investorId, assetClass],
		queryFn: commitments(investorId, assetClass),
	});

	if (isPending) return <>Loading...</>;
	if (error) return `An error has occurred: ${error.message}`;

	const total = paginatedResponse.data.reduce(
		(acc, commitment) => acc + commitment.amount,
		0,
	);

	return (
		<Table>
			<TableCaption>List of all commitments.</TableCaption>
			<TableHeader>
				<TableRow>
					<TableHead className="w-[100px]">id</TableHead>
					<TableHead>Asset Class</TableHead>
					<TableHead>Currency</TableHead>
					<TableHead className="text-right">Amount</TableHead>
				</TableRow>
			</TableHeader>
			<TableBody>
				{paginatedResponse.data.map((commitment) => (
					<TableRow key={commitment.id}>
						<TableCell className="font-medium">{commitment.id}</TableCell>
						<TableCell>{commitment.assetClass}</TableCell>
						<TableCell>{commitment.currency}</TableCell>
						<TableCell className="text-right font-medium text-primary underline underline-offset-4">
							{formatBigInt(commitment.amount)}
						</TableCell>
					</TableRow>
				))}
			</TableBody>
			<TableFooter>
				<TableRow>
					<TableCell colSpan={3}>Total</TableCell>
					<TableCell className="text-right">{formatBigInt(total)}</TableCell>
				</TableRow>
			</TableFooter>
		</Table>
	);
}

function Commitments() {
	const [assetClass, setAssetClass] = useState<number | undefined>(undefined);
	const { investorId: rawInvestorId } = useParams();

	if (!/^\d+$/.test(rawInvestorId || "")) return <Navigate to="/" />;
	const investorId = Number.parseInt(rawInvestorId || "");

	return (
		<>
			<h2 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl mb-3">
				Commitments
			</h2>
			<div className="pb-6 flex justify-center w-full">
				<AssetClassSelector
					investorId={investorId}
					assetClass={assetClass}
					setAssetClass={setAssetClass}
				/>
			</div>
			<CommitmentsTable assetClass={assetClass} investorId={investorId} />
		</>
	);
}

export default Commitments;
