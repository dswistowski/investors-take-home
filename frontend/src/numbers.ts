export function formatBigInt(number: number): string {
	if (number >= 1_000_000_000) {
		return `${(number / 1_000_000_000).toFixed(1)}B`;
	}
	if (number >= 1_000_000) {
		return `${(number / 1_000_000).toFixed(1)}M`;
	}
	return `${number}`;
}
