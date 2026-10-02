import { describe, expect, test, vi } from 'vitest';
import { trackMarketingTool } from '@/lib/marketing-analytics';

vi.mock('@/lib/marketing-analytics', () => ({ trackMarketingTool: vi.fn() }));
const mockedTool = vi.mocked(trackMarketingTool);
import { fireEvent, render, screen, cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';
import ReadinessAssessment from '@/components/marketing/ReadinessAssessment';
import ComplianceRoiCalculator from '@/components/marketing/ComplianceRoiCalculator';

afterEach(() => { cleanup(); mockedTool.mockClear(); });
describe('informational compliance tools', () => {
  test('a maximum self-score does not assert audit readiness', () => {
    render(<ReadinessAssessment />);
    for (const input of screen.getAllByRole('combobox')) fireEvent.change(input, { target: { value: '2' } });
    expect(screen.getByText('16/16 domain points')).toBeInTheDocument();
    expect(screen.getByText(/Higher reported coverage/)).toBeInTheDocument();
    expect(screen.queryByText(/Audit ready/)).not.toBeInTheDocument();
  });
  test('sales timing is separate from incremental benefit and return', () => {
    render(<ComplianceRoiCalculator />);
    fireEvent.change(screen.getByLabelText('Compliance-blocked deals'), { target: { value: '0' } });
    fireEvent.change(screen.getByLabelText('Estimated insurance savings'), { target: { value: '0' } });
    expect(screen.getByText('-100%')).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText('Sales-cycle days saved'), { target: { value: '365' } });
    expect(screen.getByText('-100%')).toBeInTheDocument();
    expect(screen.getByText(/Annualized sales timing illustration: \$1,800,000/)).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText('Sales-cycle days saved'), { target: { value: '9999' } });
    expect(screen.getByLabelText('Sales-cycle days saved')).toHaveValue(365);
  });
});

describe('tool usage measurement', () => {
  test('each tool reports one bounded usage event per mount and never its values', () => {
    render(<ReadinessAssessment />);
    const [first, second] = screen.getAllByRole('combobox');
    fireEvent.change(first, { target: { value: '2' } });
    fireEvent.change(second, { target: { value: '1' } });
    expect(mockedTool).toHaveBeenCalledTimes(1);
    expect(mockedTool).toHaveBeenCalledWith('readiness_assessment_used');
    cleanup();
    mockedTool.mockClear();
    render(<ComplianceRoiCalculator />);
    fireEvent.change(screen.getByLabelText('Average enterprise ACV'), { target: { value: '250000' } });
    fireEvent.change(screen.getByLabelText('Compliance-blocked deals'), { target: { value: '4' } });
    expect(mockedTool).toHaveBeenCalledTimes(1);
    expect(mockedTool).toHaveBeenCalledWith('roi_calculator_used');
    expect(JSON.stringify(mockedTool.mock.calls)).not.toMatch(/250000|4\b/);
  });
});
