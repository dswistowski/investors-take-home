import { Outlet, useMatches } from "react-router-dom";
import { Slash } from "lucide-react";
import {
	Breadcrumb,
	BreadcrumbItem,
	BreadcrumbLink,
	BreadcrumbList,
	BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";

export default function Root() {
	const matches = useMatches();

	const commitmentsInvestor = matches[1]?.params.investorId;
	return (
		<div className="p-6">
			<Breadcrumb className="pb-2">
				<BreadcrumbList>
					<BreadcrumbItem>
						<BreadcrumbLink href="/">Investors</BreadcrumbLink>
					</BreadcrumbItem>
					{commitmentsInvestor ? (
						<>
							<BreadcrumbSeparator>
								<Slash />
							</BreadcrumbSeparator>
							<BreadcrumbItem>
								<BreadcrumbLink href={`/${commitmentsInvestor}`}>
									Commitments
								</BreadcrumbLink>
							</BreadcrumbItem>
						</>
					) : null}
				</BreadcrumbList>
			</Breadcrumb>
			<h2 className="scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight first:mt-0 mb-6">
				Fullstack take home exercise
			</h2>

			<Outlet />
		</div>
	);
}
