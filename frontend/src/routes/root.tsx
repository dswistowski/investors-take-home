import { Outlet } from "react-router-dom";

export default function Root() {
	return (
		<div className="p-6">
			<h2 className="scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight first:mt-0 mb-6">
				Fullstack take home exercise
			</h2>
			<Outlet />
		</div>
	);
}
