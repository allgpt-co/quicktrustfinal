import { describe, expect, test } from 'vitest';
import { fireEvent, render, screen, cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';
import ReadinessAssessment from '@/components/marketing/ReadinessAssessment';
import ComplianceRoiCalculator from '@/components/marketing/ComplianceRoiCalculator';

afterEach(cleanup);
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
